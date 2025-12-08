import allure
import pytest

from tests.urls import BASE_URL
from tests.api.user_api import UserAPI
from tests.test_data import ERROR_MESSAGES, EXPECTED_STATUS_CODES, INVALID_USERS


class TestUserLogin:
    @allure.title("Вход под существующим пользователем")
    def test_login_existing_user_success(
        self, 
        user_api: UserAPI,
        registered_user
    ):
        user_data, token = registered_user
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        
        response = user_api.login_user(login_data)
        
        assert response.status_code == EXPECTED_STATUS_CODES["user_created"]
        
        response_data = response.json()
        assert response_data["success"] is True
        assert "accessToken" in response_data
        assert "refreshToken" in response_data
        assert "user" in response_data
        
        user_obj = response_data["user"]
        assert user_obj["email"] == user_data["email"]
        assert user_obj["name"] == user_data["name"]

    @allure.title("Вход с неверным логином и паролем")
    @pytest.mark.parametrize("invalid_email, invalid_password, invalid_name", INVALID_USERS)
    def test_login_invalid_credentials_fails(
        self, 
        user_api: UserAPI,
        invalid_email: str,
        invalid_password: str,
        invalid_name: str
    ):
        invalid_credentials = {
            "email": invalid_email,
            "password": invalid_password
        }
        
        response = user_api.login_user(invalid_credentials)
        
        assert response.status_code == EXPECTED_STATUS_CODES["invalid_credentials"]
        
        response_data = response.json()
        assert response_data["success"] is False
        
        expected_message = ERROR_MESSAGES["invalid_credentials"]
        actual_message = response_data.get("message", "")
        assert expected_message == actual_message