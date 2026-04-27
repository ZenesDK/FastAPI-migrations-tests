import pytest


class TestUsersAPI:
    """Модульные тесты для CRUD операций с пользователями"""

    def test_create_user_success(self, client, clean_db):
        """POST /users - успешное создание пользователя"""
        user_data = {"username": "john_doe", "age": 30}
        response = client.post("/users", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["username"] == "john_doe"
        assert data["age"] == 30

    def test_create_user_missing_field(self, client, clean_db):
        """POST /users - отсутствует обязательное поле"""
        user_data = {"username": "incomplete"}
        response = client.post("/users", json=user_data)
        assert response.status_code == 422

    def test_get_user_success(self, client, clean_db):
        """GET /users/{id} - получение существующего пользователя"""
        client.post("/users", json={"username": "jane", "age": 25})
        response = client.get("/users/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["username"] == "jane"
        assert data["age"] == 25

    def test_get_user_not_found(self, client, clean_db):
        """GET /users/{id} - пользователь не найден"""
        response = client.get("/users/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    def test_delete_user_success(self, client, clean_db):
        """DELETE /users/{id} - успешное удаление"""
        client.post("/users", json={"username": "bob", "age": 40})
        response = client.delete("/users/1")
        assert response.status_code == 204
        # Проверяем, что пользователь удалён
        get_response = client.get("/users/1")
        assert get_response.status_code == 404

    def test_delete_user_not_found(self, client, clean_db):
        """DELETE /users/{id} - попытка удалить несуществующего"""
        response = client.delete("/users/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    def test_delete_twice(self, client, clean_db):
        """DELETE /users/{id} - повторное удаление того же пользователя"""
        client.post("/users", json={"username": "alice", "age": 35})
        response1 = client.delete("/users/1")
        assert response1.status_code == 204
        response2 = client.delete("/users/1")
        assert response2.status_code == 404