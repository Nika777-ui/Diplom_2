"""
API клиент для работы с заказами
"""
import allure
from .base_api import BaseAPI
from tests.urls import ORDERS_URL, INGREDIENTS_URL


class OrderAPI(BaseAPI):
    """Клиент для API заказов"""
    
    def __init__(self, base_url: str):
        super().__init__(base_url)
    
    @allure.step("Получить список ингредиентов")
    def get_ingredients(self) -> dict:
        """Получение доступных ингредиентов"""
        response = self._get(INGREDIENTS_URL)
        return response
    
    @allure.step("Создать заказ")
    def create_order(self, ingredients: list, token: str = None) -> dict:
        """Создание нового заказа"""
        headers = {"Authorization": token} if token else {}
        order_data = {"ingredients": ingredients}
        response = self._post(ORDERS_URL, json=order_data, headers=headers)
        return response
    
    @allure.step("Получить заказы пользователя")
    def get_user_orders(self, token: str) -> dict:
        """Получение заказов конкретного пользователя"""
        headers = {"Authorization": token}
        response = self._get(ORDERS_URL, headers=headers)
        return response
    
    @allure.step("Получить все заказы")
    def get_all_orders(self) -> dict:
        """Получение всех заказов (без авторизации)"""
        response = self._get(ORDERS_URL)
        return response