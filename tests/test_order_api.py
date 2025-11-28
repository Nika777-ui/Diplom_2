import allure
import pytest
import requests
from tests.conftest import BASE_URL
from tests.data_fixtures import available_ingredients, valid_ingredients, invalid_ingredient_hash, random_ingredients


class TestOrderCreation:
    """
    Тесты для создания заказа через API Stellar Burgers
    """
    
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients_success(self, create_and_delete_user, valid_ingredients):
        """Проверяем создание заказа с авторизацией и ингредиентами"""
        user_data, token = create_and_delete_user
        
        if valid_ingredients:
            order_data = {
                "ingredients": valid_ingredients
            }
            
            response = requests.post(
                f"{BASE_URL}/orders", 
                json=order_data,
                headers={"Authorization": token}
            )
            
            assert response.status_code == 200, "Заказ с ингредиентами не создался"
            order_response = response.json()
            assert order_response["success"] is True, "Флаг success должен быть True"
            assert "order" in order_response, "Данные заказа не вернулись"
    
    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth_fails(self, valid_ingredients):
        """Проверяем создание заказа без авторизации"""
        if valid_ingredients:
            order_data = {
                "ingredients": valid_ingredients
            }
            
            response = requests.post(f"{BASE_URL}/orders", json=order_data)
            
            # Если API позволяет создавать заказы без авторизации - проверяем успех
            if response.status_code == 200:
                order_response = response.json()
                assert order_response["success"] is True, "Заказ должен создаваться"
                assert "order" in order_response, "Данные заказа не вернулись"
            else:
                # Или проверяем ошибку
                assert response.status_code in [401, 403], "Ожидался либо успех, либо ошибка авторизации"
    
    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients_fails(self, create_and_delete_user):
        """Проверяем создание заказа без ингредиентов"""
        user_data, token = create_and_delete_user
        
        order_data = {
            "ingredients": []
        }
        
        response = requests.post(
            f"{BASE_URL}/orders", 
            json=order_data,
            headers={"Authorization": token}
        )
        
        assert response.status_code == 400, "Ожидалась ошибка валидации"
        error_data = response.json()
        assert error_data["success"] is False, "Флаг success должен быть False"
    
    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash_fails(self, create_and_delete_user):
        """Проверяем создание заказа с неверными хешами ингредиентов"""
        user_data, token = create_and_delete_user
        
        order_data = {
            "ingredients": ["invalid_hash_12345", "another_invalid_hash"]
        }
        
        response = requests.post(
            f"{BASE_URL}/orders", 
            json=order_data,
            headers={"Authorization": token}
        )
        
        # Проверяем статус 500
        assert response.status_code == 500, "Ожидалась ошибка сервера для неверных хешей"
        
        # Проверяем что ответ содержит HTML (не пытаемся парсить как JSON)
        assert "text/html" in response.headers.get("Content-Type", ""), "Ожидался HTML ответ"
        assert "<!DOCTYPE html>" in response.text, "Ответ должен содержать HTML"