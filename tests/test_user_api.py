import allure
import pytest

from tests.api.user_api import UserAPI
from tests.test_data import ERROR_MESSAGES, USER_FIELDS, EXPECTED_STATUS_CODES
from tests.helpers import create_random_user_data


class TestUserCreation:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self, user_api: UserAPI, cleanup_user):
        user_data = create_random_user_data()
        
        response = user_api.create_user(user_data)
        
        assert response.status_code == EXPECTED_STATUS_CODES["user_created"]
        
        response_data = response.json()
        assert response_data["success"] is True
        assert "accessToken" in response_data
        
        token = response_data["accessToken"]
        
        profile_response = user_api.get_user_profile(token)
        assert profile_response.status_code == 200
        
        profile_data = profile_response.json()
        assert profile_data["success"] is True
        assert profile_data["user"]["email"] == user_data["email"]
        assert profile_data["user"]["name"] == user_data["name"]
        
        cleanup_user(token)

    @allure.title("Создание уже зарегистрированного пользователя")  
    def test_create_duplicate_user_fails(self, user_api: UserAPI, cleanup_user):
        user_data = create_random_user_data()
        
        first_response = user_api.create_user(user_data)
        assert first_response.status_code == EXPECTED_STATUS_CODES["user_created"]
        
        first_token = first_response.json()["accessToken"]
        cleanup_user(first_token)
        
        second_response = user_api.create_user(user_data)
        assert second_response.status_code == EXPECTED_STATUS_CODES["user_already_exists"]
        
        error_data = second_response.json()
        assert error_data["success"] is False
        assert ERROR_MESSAGES["user_already_exists"] in error_data.get("message", "")

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", USER_FIELDS)
    def test_create_user_missing_field_fails(self, missing_field, user_api: UserAPI):
        invalid_data = create_random_user_data()
        del invalid_data[missing_field]
        
        response = user_api.create_user(invalid_data)
        
        assert response.status_code == EXPECTED_STATUS_CODES["missing_required_fields"]
        
        error_data = response.json()
        assert error_data["success"] is False
        assert ERROR_MESSAGES["required_fields"] in error_data.get("message", "")