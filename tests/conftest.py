import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def client():
    """Синхронный клиент для тестов"""
    return TestClient(app)


@pytest_asyncio.fixture
async def async_client():
    """Асинхронный клиент для тестов (без запуска сервера)"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
def clean_db():
    """Очистка in-memory БД между тестами"""
    from app.routers import users
    users.db.clear()
    from itertools import count
    users._id_seq = count(start=1)
    yield
    users.db.clear()
    users._id_seq = count(start=1)