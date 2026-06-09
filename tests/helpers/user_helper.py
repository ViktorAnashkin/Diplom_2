import random
import string

def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_user_data():
    return {
        "email": f"{generate_random_string(9)}@test.ru",
        "password": generate_random_string(7),
        "name": generate_random_string(6)
    }
    