"""
Тестовые данные для API тестов
"""

# Ожидаемые сообщения об ошибках
ERROR_MESSAGES = {
    "user_already_exists": "User already exists",
    "required_fields": "Email, password and name are required fields",
    "invalid_credentials": "email or password are incorrect",
    "ingredient_ids_required": "Ingredient ids must be provided",
}

# Тестовые пользователи (неправильные данные)
INVALID_USERS = [
    # (email, password, name)
    ("wrong@test.com", "validpassword123", "Test User"),  # неверный email
    ("valid@test.com", "wrongpassword123", "Test User"),  # неверный пароль
    ("wrong@test.com", "wrongpassword123", "Test User"),  # оба неверные
]

# Невалидные данные для создания заказа
INVALID_ORDER_DATA = {
    "empty_ingredients": [],
    "invalid_hashes": ["invalid_hash_12345", "another_invalid_hash"],
    "mixed_invalid": ["61c0c5a71d1f82001bdaaa6d", "invalid_hash"],  # один валидный, один нет
}

# Поля пользователя для параметризации
USER_FIELDS = ["email", "password", "name"]

INVALID_USERS_WITH_NAME = [
    # (email, password, name)
    ("wrong@test.com", "validpassword123", "Test User"),
    ("valid@test.com", "wrongpassword123", "Test User"),
    ("wrong@test.com", "wrongpassword123", "Test User"),
]