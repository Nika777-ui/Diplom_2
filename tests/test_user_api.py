"""
Тесты для создания пользователя через API Stellar Burgers
"""
import allure
import pytest
from tests.urls import BASE_URL
from tests.api.user_api import UserAPI
from tests.test_data import ERROR_MESSAGES, USER_FIELDS
from tests.helpers import create_random_user_data


class TestUserCreation:
    """Тесты для создания пользователя"""
    
    @pytest.fixture
    def user_api(self):
        """Фикстура для API клиента пользователей"""
        return UserAPI(BASE_URL)
    
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self, user_api):
        """Проверяем успешное создание уникального пользователя"""
        # Шаг 1: Генерируем данные пользователя
        user_data = create_random_user_data()
        
        # Шаг 2: Создаем пользователя
        response = user_api.create_user(user_data)
        
        # Шаг 3: Проверяем успешное создание
        assert response.status_code == 200, "Пользователь не создался"
        
        response_data = response.json()
        assert response_data["success"] is True, "Флаг success должен быть True"
        
        # Шаг 4: Проверяем наличие токена
        token = response_data.get("accessToken")
        assert token is not None, "Токен не был получен"
        assert len(token) > 0, "Токен пустой"
        
        # Шаг 5: Проверяем что пользователь действительно создан
        profile_response = user_api.get_user_profile(token)
        assert profile_response.status_code == 200, "Не удалось получить профиль"
        
        profile_data = profile_response.json()
        assert profile_data["success"] is True, "Флаг success должен быть True"
        assert profile_data["user"]["email"] == user_data["email"], "Email не совпадает"
        assert profile_data["user"]["name"] == user_data["name"], "Name не совпадает"
        
        # Шаг 6: Удаляем пользователя (пост-условие)
        user_api.delete_user(token)
    
    @allure.title("Создание уже зарегистрированного пользователя")  
    def test_create_duplicate_user_fails(self, user_api):
        """Проверяем что нельзя создать пользователя с существующими данными"""
        # Шаг 1: Создаем первого пользователя
        user_data = create_random_user_data()
        response1 = user_api.create_user(user_data)
        
        assert response1.status_code == 200, "Первый пользователь не создался"
        assert response1.json()["success"] is True, "Флаг success должен быть True"
        
        token = response1.json().get("accessToken")
        
        # Шаг 2: Пытаемся создать такого же пользователя
        response2 = user_api.create_user(user_data)
        
        # Шаг 3: Проверяем код ответа и сообщение об ошибке
        assert response2.status_code == 403, "Ожидался статус 403 для дубликата"
        
        error_data = response2.json()
        assert error_data["success"] is False, "Флаг success должен быть False"
        assert ERROR_MESSAGES["user_already_exists"] in error_data.get("message", "")
        
        # Шаг 4: Удаляем созданного пользователя
        if token:
            user_api.delete_user(token)
    
    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", USER_FIELDS)
    def test_create_user_missing_field_fails(self, missing_field, user_api):
        """Проверяем создание пользователя без обязательных полей"""
        # Шаг 1: Создаем данные пользователя с отсутствующим полем
        invalid_data = create_random_user_data()
        del invalid_data[missing_field]
        
        # Шаг 2: Пытаемся создать пользователя
        response = user_api.create_user(invalid_data)
        
        # Шаг 3: Проверяем код ответа и тело ответа
        assert response.status_code == 403, f"Ожидался статус 403 при отсутствии поля {missing_field}"
        
        error_data = response.json()
        assert error_data["success"] is False, "Флаг success должен быть False"
        assert ERROR_MESSAGES["required_fields"] in error_data.get("message", "")