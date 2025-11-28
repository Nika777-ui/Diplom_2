import pytest
import requests
import random
from tests.conftest import BASE_URL


@pytest.fixture
def available_ingredients():
    """Фикстура для получения доступных ингредиентов"""
    response = requests.get(f"{BASE_URL}/ingredients")
    assert response.status_code == 200, "Не удалось получить ингредиенты"
    return response.json()["data"]


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


@pytest.fixture
def random_ingredients(available_ingredients):
    """Фикстура для случайного набора ингредиентов"""
    if available_ingredients:
        count = random.randint(1, min(3, len(available_ingredients)))
        return [ingredient["_id"] for ingredient in available_ingredients[:count]]
    return []