"""
Тесты для авторизации пользователя через API Stellar Burgers
"""
import allure
import pytest
from tests.urls import BASE_URL
from tests.api.user_api import UserAPI
from tests.test_data import ERROR_MESSAGES, INVALID_USERS
from tests.helpers import create_random_user_data


class TestUserLogin:
    """Тесты для авторизации пользователя"""
    
    @pytest.fixture
    def user_api(self):
        """Фикстура для API клиента пользователей"""
        return UserAPI(BASE_URL)
    
    @allure.title("Вход под существующим пользователем")
    def test_login_existing_user_success(self, user_api):
        """Проверяем успешный вход под существующим пользователем"""
        # Шаг 1: Создаем пользователя
        user_data = create_random_user_data()
        create_response = user_api.create_user(user_data)
        
        assert create_response.status_code == 200, "Не удалось создать пользователя"
        create_token = create_response.json().get("accessToken")
        
        # Шаг 2: Логинимся с правильными данными
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        
        login_response = user_api.login_user(login_data)
        
        # Шаг 3: Проверяем успешный логин
        assert login_response.status_code == 200, "Логин не удался"
        
        login_data = login_response.json()
        assert login_data["success"] is True, "Флаг success должен быть True"
        assert "accessToken" in login_data, "Токен доступа не получен"
        assert "refreshToken" in login_data, "Refresh токен не получен"
        assert login_data["user"]["email"] == user_data["email"], "Email не совпадает"
        assert login_data["user"]["name"] == user_data["name"], "Name не совпадает"
        
        # Шаг 4: Удаляем пользователя
        if create_token:
            user_api.delete_user(create_token)
    
    @allure.title("Вход с неверным логином и паролем")
    @pytest.mark.parametrize("invalid_email,invalid_password,invalid_name", INVALID_USERS)
    def test_login_invalid_credentials_fails(self, invalid_email, invalid_password, invalid_name, user_api):
        """Проверяем вход с неверными учетными данными"""
        # Шаг 1: Готовим неверные данные
        login_data = {
            "email": invalid_email,
            "password": invalid_password
        }
        
        # Шаг 2: Пытаемся авторизоваться
        response = user_api.login_user(login_data)
        
        # Шаг 3: Проверяем что логин не удался
        assert response.status_code == 401, "Ожидался статус 401 для неверных учетных данных"
        
        error_data = response.json()
        assert error_data["success"] is False, "Флаг success должен быть False"
        
        # Проверяем сообщение об ошибке (регистронезависимо)
        error_message = error_data.get("message", "").lower()
        expected_error = ERROR_MESSAGES["invalid_credentials"].lower()
        assert expected_error in error_message, "Неверное сообщение об ошибке"