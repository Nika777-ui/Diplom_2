"""
Базовый класс для API клиентов
"""
import allure
import requests
from typing import Dict, Any, Optional


class BaseAPI:
    """Базовый класс для всех API клиентов"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    @allure.step("Отправить GET запрос к {url}")
    def _get(self, url: str, headers: Optional[Dict] = None) -> requests.Response:
        """Базовый GET запрос"""
        return requests.get(url, headers=headers)
    
    @allure.step("Отправить POST запрос к {url}")
    def _post(self, url: str, json: Dict = None, headers: Optional[Dict] = None) -> requests.Response:
        """Базовый POST запрос"""
        return requests.post(url, json=json, headers=headers)
    
    @allure.step("Отправить DELETE запрос к {url}")
    def _delete(self, url: str, headers: Optional[Dict] = None) -> requests.Response:
        """Базовый DELETE запрос"""
        return requests.delete(url, headers=headers)
    
    @allure.step("Отправить PATCH запрос к {url}")
    def _patch(self, url: str, json: Dict = None, headers: Optional[Dict] = None) -> requests.Response:
        """Базовый PATCH запрос"""
        return requests.patch(url, json=json, headers=headers)