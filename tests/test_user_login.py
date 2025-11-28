import allure
import pytest
import requests
from tests.conftest import BASE_URL


class TestUserLogin:
    """
    Тесты для авторизации пользователя через API Stellar Burgers
    """
    
    @allure.title("Вход под существующим пользователем")
    def test_login_existing_user_success(self, create_and_delete_user):
        """Проверяем успешный вход под существующим пользователем"""
        user_data, register_token = create_and_delete_user
        
        # Логинимся с правильными данными
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        
        # Проверяем успешный логин
        assert response.status_code == 200, "Логин не удался"
        login_data = response.json()
        
        assert login_data["success"] is True, "Флаг success должен быть True"
        assert "accessToken" in login_data, "Токен доступа не получен"
        assert "refreshToken" in login_data, "Refresh токен не получен"
        assert login_data["user"]["email"] == user_data["email"], "Email не совпадает"
        assert login_data["user"]["name"] == user_data["name"], "Name не совпадает"
    
    @allure.title("Вход с неверным логином и паролем")
    @pytest.mark.parametrize("invalid_email,invalid_password", [
        ("wrong@test.com", "validpassword123"),  # неверный email
        ("valid@test.com", "wrongpassword123"),  # неверный пароль  
        ("wrong@test.com", "wrongpassword123")   # оба неверные
    ])
    def test_login_invalid_credentials_fails(self, invalid_email, invalid_password):
        """Проверяем вход с неверными учетными данными"""
        login_data = {
            "email": invalid_email,
            "password": invalid_password
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        
        # Проверяем что логин не удался
        assert response.status_code == 401, "Ожидался статус 401 для неверных учетных данных"
        error_data = response.json()
        
        assert error_data["success"] is False, "Флаг success должен быть False"
        assert "email or password are incorrect" in error_data.get("message", "").lower()