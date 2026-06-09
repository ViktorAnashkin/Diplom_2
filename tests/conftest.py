import allure
import pytest
import requests
from data.urls import Endpoints
from helpers.user_helper import generate_user_data

@pytest.fixture
def user_data():
    """Генерирует данные для нового пользователя"""
    return generate_user_data()

@pytest.fixture
def registered_user():
    """Создаёт и возвращает зарегистрированного пользователя, удаляет после теста"""
    user = generate_user_data()

    with allure.step("Зарегистрировать пользователя"):
        response = requests.post(Endpoints.REGISTER, json=user)
        assert response.status_code == 200, f"Регистрация не удалась: {response.status_code}"

    yield user  # Передаём данные в тест

    # Очистка после теста 
    with allure.step("Удалить тестового пользователя"):
        
        pass

@pytest.fixture
def auth_token(registered_user):
    """Возвращает токен авторизации для зарегистрированного пользователя"""
    with allure.step("Выполнить логин для получения токена"):
        login_response = requests.post(Endpoints.LOGIN, json={
            "email": registered_user["email"],
            "password": registered_user["password"]
        })
    return login_response.json().get("accessToken")
