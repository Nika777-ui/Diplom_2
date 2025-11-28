import pytest
import requests
import random
import string
from typing import Dict, Any


BASE_URL = "https://stellarburgers.education-services.ru/api"


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
    # Создаем пользователя
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    token = None
    
    if response.status_code == 200:
        token = response.json().get("accessToken")
    
    yield user_data, token  # Передаем данные в тест
    
    # После теста удаляем пользователя
    if token:
        requests.delete(f"{BASE_URL}/auth/user", headers={"Authorization": token})