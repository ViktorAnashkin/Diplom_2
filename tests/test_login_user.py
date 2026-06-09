import allure
import requests
from data.urls import Endpoints
from data.messages import ErrorMessages
from data.test_data import InvalidUserData


@allure.suite("Логин пользователя")
class TestUserLogin:

    @allure.title("Вход под существующим пользователем")
    def test_login_existing_user(self, registered_user):
        payload = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        
        with allure.step("Отправить запрос на логин с корректными данными"):
            response = requests.post(Endpoints.LOGIN, json=payload)
        
        with allure.step("Проверить, что вход выполнен успешно"):
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert "accessToken" in response.json()

    @allure.title("Вход с неверным логином и паролем")
    def test_login_invalid_credentials(self):
        with allure.step("Отправить запрос на логин с неверными данными"):
            response = requests.post(Endpoints.LOGIN, json=InvalidUserData.INVALID_LOGIN)
        
        with allure.step("Проверить, что сервер вернул ошибку 401"):
            assert response.status_code == 401
            assert response.json()["message"] == ErrorMessages.INVALID_CREDENTIALS
            