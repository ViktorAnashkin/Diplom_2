import requests
import random
import string
from data.urls import Endpoints

def generate_random_string(length):
    """Генерирует случайную строку заданной длины из букв и цифр"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def generate_user_data():
    """Генерирует данные для нового пользователя"""
    return {
        "email": f"{generate_random_string(9)}@test.ru",
        "password": generate_random_string(7),
        "name": generate_random_string(6)
    }

def register_user(user_data):
    """Регистрирует пользователя и возвращает ответ API"""
    response = requests.post(Endpoints.REGISTER, json=user_data)
    if response.status_code != 200:
        raise Exception(f"Ошибка регистрации: {response.status_code} {response.text}")
    return response.json()

def login_user(user_data):
    """Выполняет логин пользователя и возвращает токен"""
    response = requests.post(
        Endpoints.LOGIN,
        json={
            "email": user_data["email"],
            "password": user_data["password"]
        }
    )
    if response.status_code != 200:
        raise Exception(f"Ошибка авторизации: {response.status_code}")
    return response.json().get("accessToken")

def logout_user(auth_token):
    """Выполняет logout пользователя"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(Endpoints.LOGOUT, headers=headers)
    if response.status_code not in (200, 204):
        raise Exception(f"Ошибка logout: {response.status_code}")
