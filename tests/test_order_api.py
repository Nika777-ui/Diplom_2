"""
Тесты для создания заказа через API Stellar Burgers
"""
import allure
import pytest
from tests.urls import BASE_URL
from tests.api.user_api import UserAPI
from tests.api.order_api import OrderAPI
from tests.test_data import ERROR_MESSAGES, INVALID_ORDER_DATA
from tests.helpers import create_random_user_data


class TestOrderCreation:
    """Тесты для создания заказа"""
    
    @pytest.fixture
    def user_api(self):
        """Фикстура для API клиента пользователей"""
        return UserAPI(BASE_URL)
    
    @pytest.fixture
    def order_api(self):
        """Фикстура для API клиента заказов"""
        return OrderAPI(BASE_URL)
    
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients_success(self, user_api, order_api, valid_ingredients):
        """Проверяем создание заказа с авторизацией и ингредиентами"""
        # Предусловие: Ингредиенты должны быть доступны
        assert len(valid_ingredients) >= 2, "Недостаточно ингредиентов для теста"
        
        # Шаг 1: Создаем пользователя
        user_data = create_random_user_data()
        user_response = user_api.create_user(user_data)
        assert user_response.status_code == 200, "Не удалось создать пользователя"
        token = user_response.json().get("accessToken")
        
        # Шаг 2: Создаем заказ с ингредиентами
        order_data = {"ingredients": valid_ingredients}
        order_response = order_api.create_order(order_data["ingredients"], token)
        
        # Шаг 3: Проверяем успешное создание заказа
        assert order_response.status_code == 200, "Заказ с ингредиентами не создался"
        
        order_data_response = order_response.json()
        assert order_data_response["success"] is True, "Флаг success должен быть True"
        assert "order" in order_data_response, "Данные заказа не вернулись"
        assert "number" in order_data_response["order"], "Номер заказа не вернулся"
        
        # Постусловие: Удаляем пользователя
        if token:
            user_api.delete_user(token)
    
    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth_fails(self, order_api, valid_ingredients):
        """Проверяем создание заказа без авторизации (по документации)"""
        # Предусловие: Ингредиенты должны быть доступны
        assert len(valid_ingredients) >= 2, "Недостаточно ингредиентов для теста"
        
        # Шаг: Пытаемся создать заказ без авторизации
        order_data = {"ingredients": valid_ingredients}
        response = order_api.create_order(order_data["ingredients"])
        
        # Проверяем по документации: должна быть ошибка авторизации
        # Документация требует: 401 Unauthorized или 403 Forbidden
        # Примечание: фактически API может возвращать 200 (баг приложения)
        # Тест проверяет требования документации
        assert response.status_code in [401, 403], (
            f"По документации ожидалась ошибка авторизации (401/403), "
            f"но получен статус {response.status_code}. "
            f"Если API позволяет создавать заказы без авторизации - это баг."
        )
        
        # Если статус соответствует документации, проверяем тело ответа
        if response.status_code in [401, 403]:
            error_data = response.json()
            assert error_data["success"] is False, "Флаг success должен быть False"
    
    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients_fails(self, user_api, order_api):
        """Проверяем создание заказа без ингредиентов"""
        # Шаг 1: Создаем пользователя
        user_data = create_random_user_data()
        user_response = user_api.create_user(user_data)
        assert user_response.status_code == 200, "Не удалось создать пользователя"
        token = user_response.json().get("accessToken")
        
        # Шаг 2: Пытаемся создать заказ без ингредиентов
        order_data = {"ingredients": INVALID_ORDER_DATA["empty_ingredients"]}
        response = order_api.create_order(order_data["ingredients"], token)
        
        # Шаг 3: Проверяем ошибку валидации (400 Bad Request)
        assert response.status_code == 400, "Ожидалась ошибка валидации (400)"
        
        error_data = response.json()
        assert error_data["success"] is False, "Флаг success должен быть False"
        
        # Проверяем сообщение об ошибке (регистронезависимо)
        error_message = error_data.get("message", "").lower()
        assert "ingredient" in error_message, "Сообщение должно содержать информацию об ингредиентах"
        
        # Постусловие: Удаляем пользователя
        if token:
            user_api.delete_user(token)
    
    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash_fails(self, user_api, order_api):
        """Проверяем создание заказа с неверными хешами ингредиентов"""
        # Шаг 1: Создаем пользователя
        user_data = create_random_user_data()
        user_response = user_api.create_user(user_data)
        assert user_response.status_code == 200, "Не удалось создать пользователя"
        token = user_response.json().get("accessToken")
        
        # Шаг 2: Пытаемся создать заказ с невалидными хешами
        order_data = {"ingredients": INVALID_ORDER_DATA["invalid_hashes"]}
        response = order_api.create_order(order_data["ingredients"], token)
        
        # Шаг 3: Проверяем ошибку сервера (500 Internal Server Error)
        # Согласно документации API, неверные хеши должны возвращать 500
        assert response.status_code == 500, (
            f"Ожидалась ошибка сервера 500 для неверных хешей, "
            f"получен статус {response.status_code}"
        )
        
        # Постусловие: Удаляем пользователя
        if token:
            user_api.delete_user(token)