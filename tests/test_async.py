import pytest
from faker import Faker

fake = Faker()


@pytest.mark.asyncio
class TestAsyncUsersAPI:
    """Асинхронные тесты для CRUD операций с использованием Faker"""

    async def test_create_user_async(self, async_client, clean_db):
        """POST /users - асинхронное создание пользователя"""
        username = fake.user_name()
        age = fake.random_int(min=18, max=100)

        response = await async_client.post("/users", json={"username": username, "age": age})
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["username"] == username
        assert data["age"] == age

    # async def test_create_user_invalid_age_async(self, async_client, clean_db):
    #     """POST /users - невалидный возраст (отрицательный)"""
    #     response = await async_client.post("/users", json={"username": fake.user_name(), "age": -5})
    #     assert response.status_code == 422

    async def test_get_user_success_async(self, async_client, clean_db):
        """GET /users/{id} - получение существующего пользователя"""
        username = fake.user_name()
        age = fake.random_int(min=18, max=100)

        # Создаём
        create_response = await async_client.post("/users", json={"username": username, "age": age})
        user_id = create_response.json()["id"]

        # Получаем
        get_response = await async_client.get(f"/users/{user_id}")
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["username"] == username
        assert data["age"] == age

    async def test_get_user_not_found_async(self, async_client, clean_db):
        """GET /users/{id} - пользователь не найден"""
        response = await async_client.get("/users/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    async def test_delete_user_success_async(self, async_client, clean_db):
        """DELETE /users/{id} - успешное удаление"""
        # Создаём
        create_response = await async_client.post("/users", json={"username": fake.user_name(), "age": 30})
        user_id = create_response.json()["id"]

        # Удаляем
        delete_response = await async_client.delete(f"/users/{user_id}")
        assert delete_response.status_code == 204

        # Проверяем, что удалён
        get_response = await async_client.get(f"/users/{user_id}")
        assert get_response.status_code == 404

    async def test_delete_user_not_found_async(self, async_client, clean_db):
        """DELETE /users/{id} - удаление несуществующего"""
        response = await async_client.delete("/users/999")
        assert response.status_code == 404

    async def test_delete_twice_async(self, async_client, clean_db):
        """DELETE /users/{id} - повторное удаление"""
        # Создаём
        create_response = await async_client.post("/users", json={"username": fake.user_name(), "age": 25})
        user_id = create_response.json()["id"]

        # Удаляем первый раз
        response1 = await async_client.delete(f"/users/{user_id}")
        assert response1.status_code == 204

        # Удаляем второй раз
        response2 = await async_client.delete(f"/users/{user_id}")
        assert response2.status_code == 404