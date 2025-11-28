import pytest
import random
import string
from typing import Dict, Any
from tests.urls import BASE_URL
from tests.test_user_api import register_user, delete_user  # Используем наши методы с Allure steps


def generate_random_email() -> str:
    """Генерирует случайный email для тестов"""
    username = ''.join(random.choices(string.ascii_lowercase, k=8))
    return f"{username}@test.com"


def generate_random_password() -> str:
    """Генерирует случайный пароль для тестов"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


def generate_random_name() -> str:
    """Генерирует случайное имя для тестов"""
    return ''.join(random.choices(string.ascii_letters, k=8))


@pytest.fixture
def user_data() -> Dict[str, str]:
    """Генерирует данные для создания пользователя"""
    return {
        "email": generate_random_email(),
        "password": generate_random_password(), 
        "name": generate_random_name()
    }


@pytest.fixture
def create_and_delete_user(user_data: Dict[str, str]):
    """Создает пользователя и удаляет после теста"""
    # Создаем пользователя используя наш метод с Allure step
    response = register_user(user_data)
    token = None
    
    if response.status_code == 200:
        token = response.json().get("accessToken")
    
    yield user_data, token  # Передаем данные в тест
    
    # После теста удаляем пользователя используя наш метод с Allure step
    if token:
        delete_user(token)