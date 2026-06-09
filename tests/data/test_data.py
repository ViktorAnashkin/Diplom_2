# Тестовые данные для негативных проверок

class InvalidUserData:
    WITHOUT_EMAIL = {
        "password": "pass123",
        "name": "Viktor"
    }
    
    WITHOUT_PASSWORD = {
        "email": "Anashkin@test.ru",
        "name": "Viktor"
    }
    
    WITHOUT_NAME = {
        "email": "Anashkint@test.ru",
        "password": "pass123"
    }

    INVALID_LOGIN = {
        "email": "invalid@test.ru",
        "password": "invalidgpass"
    }
    