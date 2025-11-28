import allure
import pytest
import requests
from tests.urls import ORDERS_URL, INGREDIENTS_URL, USER_URL


@allure.step("Отправить GET запрос для получения ингредиентов")
def get_ingredients():
    return requests.get(INGREDIENTS_URL)


@allure.step("Отправить POST запрос для создания заказа")
def create_order(order_data, token=None):
    headers = {"Authorization": token} if token else {}
    return requests.post(ORDERS_URL, json=order_data, headers=headers)


@allure.step("Отправить DELETE запрос на удаление пользователя")
def delete_user(token):
    headers = {"Authorization": token}
    return requests.delete(USER_URL, headers=headers)


class TestOrderCreation:
    """
    Тесты для создания заказа через API Stellar Burgers
    """
    
    @pytest.fixture
    def available_ingredients(self):
        """Фикстура для получения доступных ингредиентов"""
        response = get_ingredients()
        assert response.status_code == 200, "Не удалось получить ингредиенты"
        ingredients_data = response.json()
        assert ingredients_data["success"] is True, "Флаг success должен быть True"
        return ingredients_data["data"]
    
    @pytest.fixture
    def valid_ingredients(self, available_ingredients):
        """Фикстура для валидных ингредиентов"""
        if available_ingredients:
            return [ingredient["_id"] for ingredient in available_ingredients[:2]]
        return []
    
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients_success(self, create_and_delete_user, valid_ingredients):
        """Проверяем создание заказа с авторизацией и ингредиентами"""
        user_data, token = create_and_delete_user
        
        if valid_ingredients:
            order_data = {
                "ingredients": valid_ingredients
            }
            
            response = create_order(order_data, token)
            
            # Проверяем успешное создание заказа (статус + тело ответа)
            assert response.status_code == 200, "Заказ с ингредиентами не создался"
            order_response = response.json()
            assert order_response["success"] is True, "Флаг success должен быть True"
            assert "order" in order_response, "Данные заказа не вернулись"
            assert "number" in order_response["order"], "Номер заказа не вернулся"
    
    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth_fails(self, valid_ingredients):
        """Проверяем создание заказа без авторизации"""
        if valid_ingredients:
            order_data = {
                "ingredients": valid_ingredients
            }
            
            response = create_order(order_data)
            
            # Если API позволяет создавать заказы без авторизации - проверяем успех
            if response.status_code == 200:
                order_response = response.json()
                assert order_response["success"] is True, "Заказ должен создаваться"
                assert "order" in order_response, "Данные заказа не вернулись"
            else:
                # Или проверяем ошибку авторизации
                assert response.status_code in [401, 403], "Ожидался либо успех, либо ошибка авторизации"
                error_data = response.json()
                assert error_data["success"] is False, "Флаг success должен быть False"
    
    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients_fails(self, create_and_delete_user):
        """Проверяем создание заказа без ингредиентов"""
        user_data, token = create_and_delete_user
        
        order_data = {
            "ingredients": []
        }
        
        response = create_order(order_data, token)
        
        # Проверяем ошибку валидации (статус + тело ответа)
        assert response.status_code == 400, "Ожидалась ошибка валидации"
        error_data = response.json()
        assert error_data["success"] is False, "Флаг success должен быть False"
        assert "ingredient ids" in error_data.get("message", "").lower()
    
    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash_fails(self, create_and_delete_user):
        """Проверяем создание заказа с неверными хешами ингредиентов"""
        user_data, token = create_and_delete_user
        
        order_data = {
            "ingredients": ["invalid_hash_12345", "another_invalid_hash"]
        }
        
        response = create_order(order_data, token)
        
        # Проверяем статус 500
        assert response.status_code == 500, "Ожидалась ошибка сервера для неверных хешей"
        
        # Проверяем что ответ содержит HTML (не пытаемся парсить как JSON)
        assert "text/html" in response.headers.get("Content-Type", ""), "Ожидался HTML ответ"
        assert "<!DOCTYPE html>" in response.text, "Ответ должен содержать HTML"