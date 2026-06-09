import allure
import pytest
import requests
from data.urls import Endpoints
from data.messages import ErrorMessages
from data.test_data import InvalidUserData
from helpers.user_helper import generate_user_data


@allure.suite("Создание пользователя")
class TestUserCreation:

    @allure.title("Создать уникального пользователя")
    def test_create_unique_user(self):
        user = generate_user_data()
        
        with allure.step("Отправить запрос на создание пользователя"):
            response = requests.post(Endpoints.REGISTER, json=user)
        
        with allure.step("Проверить, что пользователь создан успешно"):
            assert response.status_code == 200
            assert response.json()["success"] is True

    @allure.title("Создать пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, registered_user):
        with allure.step("Отправить запрос на регистрацию уже существующего пользователя"):
            response = requests.post(Endpoints.REGISTER, json=registered_user)
        
        with allure.step("Проверить, что сервер вернул ошибку 403"):
            assert response.status_code == 403
            assert response.json()["message"] == ErrorMessages.USER_ALREADY_EXISTS

    @allure.title("Создать пользователя без одного из обязательных полей")
    @pytest.mark.parametrize("missing_field, user_data, expected_message", [
        (
            "email",
            InvalidUserData.WITHOUT_EMAIL,
            ErrorMessages.REQUIRED_FIELDS
        ),
        (
            "password",
            InvalidUserData.WITHOUT_PASSWORD,
            ErrorMessages.REQUIRED_FIELDS
        ),
        (
            "name",
            InvalidUserData.WITHOUT_NAME,
            ErrorMessages.REQUIRED_FIELDS
        ),
    ])
    def test_create_user_missing_field(self, missing_field, user_data, expected_message):
        with allure.step(f"Отправить запрос на создание пользователя без поля '{missing_field}'"):
            response = requests.post(Endpoints.REGISTER, json=user_data)
        
        with allure.step("Проверить, что сервер вернул ошибку 403"):
            assert response.status_code == 403
            assert expected_message in response.json()["message"]
            