import allure
import pytest
from helpers.user_helper import (
    generate_user_data,
    register_user,
    login_user,
    logout_user
)
from data.urls import Endpoints
import requests

@pytest.fixture
def user_data():
    return generate_user_data()

@pytest.fixture
def registered_user():
    user = generate_user_data()
    with allure.step("Зарегистрировать пользователя"):
        register_user(user)
    yield user
    with allure.step("Выполнить logout пользователя"):
        try:
            token = login_user(user)
            logout_user(token)
        except Exception as e:
            print(f"Предупреждение: не удалось выполнить logout: {e}")

@pytest.fixture
def auth_token(registered_user):
    with allure.step("Получить токен авторизации"):
        return login_user(registered_user)

@pytest.fixture
def cleanup_user():
    users_to_cleanup = []

    def _register_user_for_cleanup(user_data):
        users_to_cleanup.append(user_data)

    yield _register_user_for_cleanup

    for user in users_to_cleanup:
        try:
            token = login_user(user)
            logout_user(token)
            headers = {"Authorization": token}
            response = requests.delete(Endpoints.DELETE_USER, headers=headers)
            if response.status_code not in (200, 204, 404):
                print(f"Предупреждение: не удалось удалить пользователя {user.get('email', 'unknown')}: статус {response.status_code}")
        except Exception as e:
            print(f"Ошибка при очистке пользователя {user.get('email', 'unknown')}: {e}")
