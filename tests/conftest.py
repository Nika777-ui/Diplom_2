import pytest
from typing import Dict, Tuple, Optional, List
from tests.urls import BASE_URL
from tests.helpers import create_random_user_data
from tests.test_data import INVALID_INGREDIENT_HASHES


@pytest.fixture
def user_data() -> Dict[str, str]:
    """Генерирует данные для создания пользователя"""
    return create_random_user_data()


@pytest.fixture
def registered_user():
    """
    Создает пользователя для теста и удаляет после выполнения.
    Возвращает: (user_data, token)
    """
    from tests.api.user_api import UserAPI
    user_api = UserAPI(BASE_URL)
    
    # Создаем пользователя
    user_data = create_random_user_data()
    response = user_api.create_user(user_data)
    
    # Извлекаем токен, если пользователь создан успешно
    token = None
    if response.status_code == 200:
        token = response.json().get("accessToken")
    
    yield user_data, token
    
    # После теста удаляем пользователя (если был создан)
    if token:
        user_api.delete_user(token)


@pytest.fixture
def authorized_user():
    """
    Создает и авторизует пользователя.
    Возвращает: (user_data, token, auth_token)
    """
    from tests.api.user_api import UserAPI
    user_api = UserAPI(BASE_URL)
    
    # Создаем пользователя
    user_data = create_random_user_data()
    create_response = user_api.create_user(user_data)
    
    token = None
    auth_token = None
    
    if create_response.status_code == 200:
        token = create_response.json().get("accessToken")
        
        # Авторизуемся для получения auth_token
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        login_response = user_api.login_user(login_data)
        if login_response.status_code == 200:
            auth_token = login_response.json().get("accessToken")
    
    yield user_data, token, auth_token
    
    # После теста удаляем пользователя
    if token:
        user_api.delete_user(token)


@pytest.fixture
def available_ingredients() -> List[Dict]:
    """
    Получает доступные ингредиенты.
    Возвращает пустой список при ошибке (не падает).
    """
    from tests.api.order_api import OrderAPI
    order_api = OrderAPI(BASE_URL)
    response = order_api.get_ingredients()
    
    if response.status_code == 200:
        ingredients_data = response.json()
        return ingredients_data.get("data", [])
    return []


@pytest.fixture
def valid_ingredients(available_ingredients) -> List[str]:
    """Возвращает валидные ингредиенты (первые 2)"""
    if available_ingredients and len(available_ingredients) >= 2:
        return [ingredient["_id"] for ingredient in available_ingredients[:2]]
    return []


@pytest.fixture
def user_api():
    """Фикстура для API клиента пользователей"""
    from tests.api.user_api import UserAPI
    return UserAPI(BASE_URL)


@pytest.fixture
def order_api():
    """Фикстура для API клиента заказов"""
    from tests.api.order_api import OrderAPI
    return OrderAPI(BASE_URL)


@pytest.fixture
def cleanup_user():
    """
    Фикстура для очистки пользователя после теста.
    Собирает токены и удаляет пользователей в teardown.
    """
    tokens_to_cleanup = []
    
    def add_token_for_cleanup(token: str):
        if token:
            tokens_to_cleanup.append(token)
    
    yield add_token_for_cleanup
    
    # После теста удаляем всех созданных пользователей
    from tests.api.user_api import UserAPI
    user_api = UserAPI(BASE_URL)
    for token in tokens_to_cleanup:
        try:
            user_api.delete_user(token)
        except:
            pass  # Игнорируем ошибки при удалении