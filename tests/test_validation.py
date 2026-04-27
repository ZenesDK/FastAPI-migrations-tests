import pytest


def test_register_user_success(client):
    """Успешная регистрация с валидными данными"""
    user_data = {
        "username": "testuser",
        "age": 25,
        "email": "test@example.com",
        "password": "securepass123",
        "phone": "+1234567890"
    }
    response = client.post("/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User testuser registered successfully"
    assert data["data"]["username"] == "testuser"
    assert data["data"]["age"] == 25
    assert data["data"]["email"] == "test@example.com"


def test_register_user_age_too_young(client):
    """Ошибка: возраст меньше или равен 18 (должно быть >18)"""
    user_data = {
        "username": "younguser",
        "age": 18,
        "email": "young@example.com",
        "password": "securepass123",
        "phone": "+1234567890"
    }
    response = client.post("/register", json=user_data)
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "Validation error"
    assert "Invalid input data" in data["message"]


def test_register_user_invalid_email(client):
    """Ошибка: невалидный email"""
    user_data = {
        "username": "testuser2",
        "age": 25,
        "email": "not-an-email",
        "password": "securepass123",
        "phone": "+1234567890"
    }
    response = client.post("/register", json=user_data)
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "Validation error"


def test_register_user_password_too_short(client):
    """Ошибка: пароль короче 8 символов"""
    user_data = {
        "username": "testuser3",
        "age": 25,
        "email": "test3@example.com",
        "password": "short",
        "phone": "+1234567890"
    }
    response = client.post("/register", json=user_data)
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "Validation error"


def test_register_user_password_too_long(client):
    """Ошибка: пароль длиннее 16 символов"""
    user_data = {
        "username": "testuser4",
        "age": 25,
        "email": "test4@example.com",
        "password": "thispasswordiswaytoolong123",
        "phone": "+1234567890"
    }
    response = client.post("/register", json=user_data)
    assert response.status_code == 422


def test_register_user_missing_required_field(client):
    """Ошибка: отсутствует обязательное поле username"""
    user_data = {
        "age": 25,
        "email": "test5@example.com",
        "password": "securepass123"
    }
    response = client.post("/register", json=user_data)
    assert response.status_code == 422


def test_register_user_without_phone(client):
    """Успешная регистрация без поля phone (используется значение по умолчанию)"""
    user_data = {
        "username": "nophone",
        "age": 30,
        "email": "nophone@example.com",
        "password": "securepass123"
    }
    response = client.post("/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["phone"] == "Unknown"