import allure
import pytest
import requests
from tests.urls import REGISTER_URL, USER_URL


@allure.step("Отправить POST запрос на создание пользователя")
def register_user(user_data):
    return requests.post(REGISTER_URL, json=user_data)


@allure.step("Отправить DELETE запрос на удаление пользователя")
def delete_user(token):
    headers = {"Authorization": token}
    return requests.delete(USER_URL, headers=headers)


@allure.step("Отправить GET запрос для получения профиля пользователя")
def get_user_profile(token):
    headers = {"Authorization": token}
    return requests.get(USER_URL, headers=headers)


class TestUserCreation:
    """
    Тесты для создания пользователя через API Stellar Burgers
    """
    
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self, create_and_delete_user):
        """Проверяем успешное создание уникального пользователя"""
        user_data, token = create_and_delete_user
        
        # Проверяем что пользователь создан и получен токен
        assert token is not None, "Токен не был получен"
        assert len(token) > 0, "Токен пустой"
        
        # Проверяем что пользователь действительно создан через запрос к профилю
        profile_response = get_user_profile(token)
        assert profile_response.status_code == 200, "Не удалось получить профиль"
        
        profile_data = profile_response.json()
        assert profile_data["success"] is True, "Флаг success должен быть True"
        assert profile_data["user"]["email"] == user_data["email"], "Email не совпадает"
        assert profile_data["user"]["name"] == user_data["name"], "Name не совпадает"
    
    @allure.title("Создание уже зарегистрированного пользователя")  
    def test_create_duplicate_user_fails(self, user_data):
        """Проверяем что нельзя создать пользователя с существующими данными"""
        # Сначала создаем пользователя
        response1 = register_user(user_data)
        assert response1.status_code == 200, "Первый пользователь не создался"
        assert response1.json()["success"] is True, "Флаг success должен быть True"
        
        # Пытаемся создать такого же пользователя
        response2 = register_user(user_data)
        
        # Проверяем код ответа и сообщение об ошибке
        assert response2.status_code == 403, "Ожидался статус 403 для дубликата"
        error_data = response2.json()
        assert error_data["success"] is False, "Флаг success должен быть False"
        assert "User already exists" in error_data.get("message", "")
        
        # Удаляем созданного пользователя
        token = response1.json().get("accessToken")
        if token:
            delete_user(token)
    
    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field_fails(self, missing_field, user_data):
        """Проверяем создание пользователя без обязательных полей"""
        # Удаляем одно поле
        invalid_data = user_data.copy()
        del invalid_data[missing_field]
        
        # Пытаемся создать пользователя
        response = register_user(invalid_data)
        
        # Проверяем код ответа и тело ответа
        assert response.status_code == 403, f"Ожидался статус 403 при отсутствии поля {missing_field}"
        error_data = response.json()
        assert error_data["success"] is False, "Флаг success должен быть False"
        assert "Email, password and name are required fields" in error_data.get("message", "")