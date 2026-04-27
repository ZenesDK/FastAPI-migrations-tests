import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def clean_db():
    """Очистка in-memory БД между тестами"""
    from app.routers import users
    users.db.clear()
    # Сбрасываем счётчик ID (если нужно)
    from itertools import count
    users._id_seq = count(start=1)
    yield
    users.db.clear()
    users._id_seq = count(start=1)