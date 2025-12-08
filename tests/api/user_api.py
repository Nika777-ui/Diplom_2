"""
API клиент для работы с пользователями
"""
import allure
from .base_api import BaseAPI
from tests.urls import REGISTER_URL, LOGIN_URL, USER_URL


class UserAPI(BaseAPI):
    """Клиент для API пользователей"""
    
    def __init__(self, base_url: str):
        super().__init__(base_url)
    
    @allure.step("Создать пользователя")
    def create_user(self, user_data: dict) -> dict:
        """Регистрация нового пользователя"""
        response = self._post(REGISTER_URL, json=user_data)
        return response
    
    @allure.step("Авторизовать пользователя")
    def login_user(self, login_data: dict) -> dict:
        """Авторизация пользователя"""
        response = self._post(LOGIN_URL, json=login_data)
        return response
    
    @allure.step("Удалить пользователя")
    def delete_user(self, token: str) -> dict:
        """Удаление пользователя"""
        headers = {"Authorization": token}
        response = self._delete(USER_URL, headers=headers)
        return response
    
    @allure.step("Получить профиль пользователя")
    def get_user_profile(self, token: str) -> dict:
        """Получение профиля пользователя"""
        headers = {"Authorization": token}
        response = self._get(USER_URL, headers=headers)
        return response
    
    @allure.step("Изменить данные пользователя")
    def update_user_profile(self, token: str, user_data: dict) -> dict:
        """Обновление данных пользователя"""
        headers = {"Authorization": token}
        response = self._patch(USER_URL, json=user_data, headers=headers)
        return response