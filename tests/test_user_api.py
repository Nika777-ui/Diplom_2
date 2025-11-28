import allure
import pytest
import requests
from tests.conftest import BASE_URL


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
        
        # Можно добавить проверку что пользователь действительно создан
        # через запрос к профилю
        profile_response = requests.get(
            f"{BASE_URL}/auth/user", 
            headers={"Authorization": token}
        )
        assert profile_response.status_code == 200, "Не удалось получить профиль"
        
        profile_data = profile_response.json()
        assert profile_data["user"]["email"] == user_data["email"]
        assert profile_data["user"]["name"] == user_data["name"]
    
    @allure.title("Создание уже зарегистрированного пользователя")  
    def test_create_duplicate_user_fails(self, user_data):
        """Проверяем что нельзя создать пользователя с существующими данными"""
        # Сначала создаем пользователя
        response1 = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        assert response1.status_code == 200, "Первый пользователь не создался"
        
        # Пытаемся создать такого же пользователя
        response2 = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        
        # Проверяем код ответа и сообщение об ошибке
        assert response2.status_code == 403, "Ожидался статус 403 для дубликата"
        error_data = response2.json()
        assert "success" in error_data
        assert error_data["success"] is False
        assert "User already exists" in error_data.get("message", "")
        
        # Удаляем созданного пользователя
        token = response1.json().get("accessToken")
        if token:
            requests.delete(f"{BASE_URL}/auth/user", headers={"Authorization": token})
    
    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field_fails(self, missing_field, user_data):
        """Проверяем создание пользователя без обязательных полей"""
        # Удаляем одно поле
        invalid_data = user_data.copy()
        del invalid_data[missing_field]
        
        # Пытаемся создать пользователя
        response = requests.post(f"{BASE_URL}/auth/register", json=invalid_data)
        
        # Проверяем код ответа
        assert response.status_code == 403, f"Ожидался статус 403 при отсутствии поля {missing_field}"
        error_data = response.json()
        assert "success" in error_data
        assert error_data["success"] is False
        assert "Email, password and name are required fields" in error_data.get("message", "")