import allure
import requests
from data.urls import Endpoints
from data.ingredients import VALID_INGREDIENTS, INVALID_HASH
from data.messages import ErrorMessages


@allure.suite("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, auth_token):
        headers = {"Authorization": auth_token}
        payload = {"ingredients": VALID_INGREDIENTS}
        
        with allure.step("Отправить запрос на создание заказа с авторизацией"):
            response = requests.post(Endpoints.ORDERS, json=payload, headers=headers)
        
        with allure.step("Проверить, что заказ создан успешно"):
            assert response.status_code == 200
            assert response.json()["success"] is True

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self):
        payload = {"ingredients": VALID_INGREDIENTS}
        
        with allure.step("Отправить запрос на создание заказа без авторизации"):
            response = requests.post(Endpoints.ORDERS, json=payload)
        
        with allure.step("Проверить, что заказ создан успешно"):
            assert response.status_code == 200
            assert response.json()["success"] is True

    @allure.title("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients(self, auth_token):
        headers = {"Authorization": auth_token}
        payload = {"ingredients": VALID_INGREDIENTS}
        
        with allure.step("Отправить запрос на создание заказа с ингредиентами"):
            response = requests.post(Endpoints.ORDERS, json=payload, headers=headers)
        
        with allure.step("Проверить, что в заказе есть ингредиенты"):
            assert response.status_code == 200
            assert len(response.json()["order"]["ingredients"]) > 0

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, auth_token):
        headers = {"Authorization": auth_token}
        payload = {"ingredients": []}
        
        with allure.step("Отправить запрос на создание заказа без ингредиентов"):
            response = requests.post(Endpoints.ORDERS, json=payload, headers=headers)
        
        with allure.step("Проверить, что сервер вернул ошибку 400"):
            assert response.status_code == 400
            assert response.json()["message"] == ErrorMessages.INGREDIENTS_REQUIRED

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_hash(self, auth_token):
        headers = {"Authorization": auth_token}
        payload = {"ingredients": [INVALID_HASH]}
        
        with allure.step("Отправить запрос на создание заказа с неверным хешем ингредиентов"):
            response = requests.post(Endpoints.ORDERS, json=payload, headers=headers)
        
        with allure.step("Проверить, что сервер вернул ошибку"):
            assert response.status_code in [400, 500]
            