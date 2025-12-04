"""
Фикстуры для API тестов
"""
import pytest
import requests
from typing import Dict, Tuple
from tests.urls import BASE_URL
from tests.helpers import create_random_user_data, extract_token_from_response


@pytest.fixture
def user_data() -> Dict[str, str]:
    """Генерирует данные для создания пользователя"""
    return create_random_user_data()


@pytest.fixture
def create_and_delete_user():
    """
    Создает пользователя для теста и удаляет после выполнения
    ВНИМАНИЕ: эту фикстуру НЕ использовать в тестах создания пользователя!
    """
    from tests.api.user_api import UserAPI
    
    user_api = UserAPI(BASE_URL)
    user_data = create_random_user_data()
    
    # Создаем пользователя
    response = user_api.create_user(user_data)
    token = extract_token_from_response(response)
    
    yield user_data, token  # Передаем данные в тест
    
    # После теста удаляем пользователя
    if token:
        user_api.delete_user(token)


@pytest.fixture
def available_ingredients():
    """Фикстура для получения доступных ингредиентов"""
    from tests.api.order_api import OrderAPI
    
    order_api = OrderAPI(BASE_URL)
    response = order_api.get_ingredients()
    
    assert response.status_code == 200, "Не удалось получить ингредиенты"
    ingredients_data = response.json()
    return ingredients_data.get("data", [])


@pytest.fixture
def valid_ingredients(available_ingredients):
    """Фикстура для валидных ингредиентов"""
    if available_ingredients:
        return [ingredient["_id"] for ingredient in available_ingredients[:2]]
    return []


@pytest.fixture  
def invalid_ingredient_hash():
    """Фикстура для невалидного хеша ингредиента"""
    return "invalid_hash_12345"