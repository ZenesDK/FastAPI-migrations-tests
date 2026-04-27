from app.exceptions import CustomExceptionA, CustomExceptionB


def test_custom_exception_a(client):
    """Тест кастомного исключения A (403 Forbidden)"""
    response = client.get("/forbidden")
    assert response.status_code == 403
    data = response.json()
    assert data["error"] == "ForbiddenError"
    assert "Access denied" in data["message"]


def test_custom_exception_b(client):
    """Тест кастомного исключения B (404 Not Found)"""
    response = client.get("/not-found")
    assert response.status_code == 404
    data = response.json()
    assert data["error"] == "NotFoundError"
    assert "does not exist" in data["message"]