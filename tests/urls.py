"""
Модуль с URL эндпоинтов API Stellar Burgers
"""

BASE_URL = "https://stellarburgers.education-services.ru/api"

# Auth endpoints
REGISTER_URL = f"{BASE_URL}/auth/register"
LOGIN_URL = f"{BASE_URL}/auth/login" 
USER_URL = f"{BASE_URL}/auth/user"
LOGOUT_URL = f"{BASE_URL}/auth/logout"
TOKEN_URL = f"{BASE_URL}/auth/token"

# Order endpoints
ORDERS_URL = f"{BASE_URL}/orders"
INGREDIENTS_URL = f"{BASE_URL}/ingredients"