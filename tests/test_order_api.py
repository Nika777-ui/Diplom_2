import allure
import pytest

from tests.urls import BASE_URL
from tests.api.order_api import OrderAPI
from tests.test_data import ERROR_MESSAGES, INVALID_ORDER_DATA, EXPECTED_STATUS_CODES


class TestOrderCreation:
    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(
        self, 
        order_api: OrderAPI,
        registered_user,
        valid_ingredients
    ):
        _, token = registered_user
        
        response = order_api.create_order(valid_ingredients, token)
        
        assert response.status_code == EXPECTED_STATUS_CODES["order_created"]
        
        response_data = response.json()
        assert response_data["success"] is True

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(
        self, 
        order_api: OrderAPI,
        valid_ingredients
    ):
        response = order_api.create_order(valid_ingredients)
        
        assert response.status_code == EXPECTED_STATUS_CODES["order_unauthorized"]

    @allure.title("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients(
        self, 
        order_api: OrderAPI,
        registered_user,
        valid_ingredients
    ):
        _, token = registered_user
        
        response = order_api.create_order(valid_ingredients, token)
        
        assert response.status_code == EXPECTED_STATUS_CODES["order_created"]
        
        response_data = response.json()
        assert response_data["success"] is True
        assert "order" in response_data
        assert "number" in response_data["order"]
        assert "ingredients" in response_data["order"]

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(
        self,
        order_api: OrderAPI,
        registered_user
    ):
        _, token = registered_user
        
        response = order_api.create_order([], token)
        
        assert response.status_code == EXPECTED_STATUS_CODES["order_no_ingredients"]
        
        response_data = response.json()
        assert response_data["success"] is False
        assert ERROR_MESSAGES["ingredient_ids_required"] in response_data.get("message", "")

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash(
        self,
        order_api: OrderAPI,
        registered_user
    ):
        _, token = registered_user
        invalid_hashes = INVALID_ORDER_DATA["invalid_hashes"]
        
        response = order_api.create_order(invalid_hashes, token)
        
        assert response.status_code == EXPECTED_STATUS_CODES["order_invalid_ingredients"]