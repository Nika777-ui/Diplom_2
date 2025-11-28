import allure
import pytest
import requests
from tests.urls import LOGIN_URL, REGISTER_URL, USER_URL


@allure.step("Отправить POST запрос на авторизацию пользователя")
def login_user(login_data):
    return requests.post(LOGIN_URL, json=login_data)


@allure.step("Отправить POST запрос на создание пользователя")
def register_user(user_data):
    return requests.post(REGISTER_URL, json=user_data)


@allure.step("Отправить DELETE запрос на удаление пользователя")
def delete_user(token):
    headers = {"Authorization": token}
    return requests.delete(USER_URL, headers=headers)


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
        
        response = login_user(login_data)
        
        # Проверяем успешный логин (статус + тело ответа)
        assert response.status_code == 200, "Логин не удался"
        login_response = response.json()
        
        assert login_response["success"] is True, "Флаг success должен быть True"
        assert "accessToken" in login_response, "Токен доступа не получен"
        assert "refreshToken" in login_response, "Refresh токен не получен"
        assert login_response["user"]["email"] == user_data["email"], "Email не совпадает"
        assert login_response["user"]["name"] == user_data["name"], "Name не совпадает"
    
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
        
        response = login_user(login_data)
        
        # Проверяем что логин не удался (статус + тело ответа)
        assert response.status_code == 401, "Ожидался статус 401 для неверных учетных данных"
        error_data = response.json()
        
        assert error_data["success"] is False, "Флаг success должен быть False"
        assert "email or password are incorrect" in error_data.get("message", "").lower()