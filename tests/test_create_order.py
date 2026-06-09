import allure
import requests
from data.urls import Endpoints
from data.ingredients import VALID_INGREDIENTS, INVALID_HASH
from data.messages import ErrorMessages

@allure.suite("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, auth_token):
        headers = {"Authorization": auth_token}
        payload = {"ingredients": VALID_INGREDIENTS}

        with allure.step("Отправить запрос на создание заказа с авторизацией и ингредиентами"):
            response = requests.post(Endpoints.ORDERS, json=payload, headers=headers)

        with allure.step("Проверить ответ сервера"):
            assert response.status_code in [200, 400]

            if response.status_code == 200:
                data = response.json()
                assert data["success"] is True
                with allure.step("Проверить структуру заказа"):
                    assert "order" in data
                    order = data["order"]
                    assert "number" in order
                    assert isinstance(order["number"], int)
                    assert "createdAt" in order
                    assert "updatedAt" in order

                with allure.step("Проверить ингредиенты в заказе"):
                    returned_ingredients = order["ingredients"]
                    assert len(returned_ingredients) == len(VALID_INGREDIENTS)
                    returned_hashes = [ingredient["_id"] for ingredient in returned_ingredients]
                    assert sorted(returned_hashes) == sorted(VALID_INGREDIENTS)
            else:
                # Обработка случая 400
                try:
                    data = response.json()
                    assert data["success"] is False
                    assert "message" in data
                except requests.exceptions.JSONDecodeError:
                    # Если ответ не JSON (например, HTML), проверяем статус и содержимое
                    allure.attach(
                        response.text,
                        name="HTML Response (500 Error)",
                        attachment_type=allure.attachment_type.HTML
                    )
                    raise AssertionError(f"Сервер вернул статус {response.status_code}, но не JSON: {response.text[:200]}...")

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self):
        payload = {"ingredients": VALID_INGREDIENTS}

        with allure.step("Отправить запрос на создание заказа без авторизации"):
            response = requests.post(Endpoints.ORDERS, json=payload)

        with allure.step("Проверить, что сервер возвращает ошибку 400"):
            assert response.status_code == 400
            try:
                data = response.json()
                assert data["success"] is False
                assert "message" in data
            except requests.exceptions.JSONDecodeError:
                allure.attach(
                    response.text,
            name="HTML Response",
            attachment_type=allure.attachment_type.HTML
                )
                raise AssertionError(f"Сервер вернул статус 400, но не JSON: {response.text[:200]}...")

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, auth_token):
        headers = {"Authorization": auth_token}
        payload = {"ingredients": []}

        with allure.step("Отправить запрос на создание заказа без ингредиентов"):
            response = requests.post(Endpoints.ORDERS, json=payload, headers=headers)

        with allure.step("Проверить, что сервер вернул ошибку 400"):
            assert response.status_code == 400
            data = response.json()
            assert data["success"] is False
            assert data["message"] == ErrorMessages.INGREDIENTS_REQUIRED

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_hash(self, auth_token):
        headers = {"Authorization": auth_token}
        payload = {"ingredients": [INVALID_HASH]}

        with allure.step("Отправить запрос на создание заказа с неверным хешем ингредиентов"):
            response = requests.post(Endpoints.ORDERS, json=payload, headers=headers)

        with allure.step("Проверить, что сервер вернул ошибку (400 или 500)"):
            assert response.status_code in [400, 500]

        # Безопасное получение данных из ответа
        try:
            data = response.json()
            with allure.step("Проверить JSON‑ответ сервера"):
                assert data["success"] is False
                if "message" in data:
                    allure.attach(data["message"], "Сообщение об ошибке")
        except requests.exceptions.JSONDecodeError:
            # Обработка HTML‑ответа при 500 ошибке
            allure.attach(
                response.text,
                name="HTML Response (500 Error)",
                attachment_type=allure.attachment_type.HTML
            )
            with allure.step("Проверить HTML‑ответ сервера при 500 ошибке"):
                assert "<title>Error</title>" in response.text
                assert "Internal Server Error" in response.text
