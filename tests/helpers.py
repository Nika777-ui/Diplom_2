"""
Вспомогательные функции для тестов
"""
import random
import string
from typing import Dict


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


def create_random_user_data() -> Dict[str, str]:
    """Создает случайные данные пользователя"""
    return {
        "email": generate_random_email(),
        "password": generate_random_password(),
        "name": generate_random_name()
    }


def extract_token_from_response(response) -> str:
    """Извлекает токен из ответа API"""
    if response.status_code == 200:
        return response.json().get("accessToken")
    return None