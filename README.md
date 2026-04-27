## Задание 9.1 - Миграции Alembic

### Выполненные шаги:

1. **Установлен Alembic** и настроен для SQLite
2. **Создана модель Product** с полями: `id`, `title`, `price`, `count`
3. **Создана первая миграция** для создания таблицы products
4. **Применена миграция** и добавлены 2 записи (Laptop, Mouse)
5. **Добавлено поле `description`** в модель Product
6. **Создана вторая миграция** с добавлением колонки `description` (NOT NULL, default='')
7. **Применена миграция** - таблица обновлена без потери данных

### Команды для воспроизведения:

```bash
# Применить все миграции
alembic upgrade head

# Создать новую миграцию
alembic revision --autogenerate -m "description"

# Просмотр истории миграций
alembic history

# Проверка текущей версии
alembic current

Вот раздел для README.md по заданию 10.1:
```

## Задание 10.1 - Кастомная обработка ошибок

### Реализовано:

1. **Кастомные классы исключений:**
   - `CustomExceptionA` (403 Forbidden)
   - `CustomExceptionB` (404 Not Found)

2. **Обработчики исключений** через `@app.exception_handler`

3. **Модель ошибки Pydantic** `ErrorResponse` для единого формата ответа

4. **Эндпоинты для тестирования:**
   - `GET /forbidden` — вызывает `CustomExceptionA`
   - `GET /not-found` — вызывает `CustomExceptionB`

### Примеры ответов:

**403 Forbidden:**
```json
{
  "status_code": 403,
  "error": "ForbiddenError",
  "message": "Access denied: insufficient permissions"
}
```

**404 Not Found:**
```json
{
  "status_code": 404,
  "error": "NotFoundError",
  "message": "The requested resource does not exist"
}
```

### Тестирование:

```bash
# Ручная проверка
curl http://localhost:8000/forbidden
curl http://localhost:8000/not-found

# Автотесты
pytest tests/test_errors.py -v
```

### Результат тестов:
```
tests/test_errors.py::test_custom_exception_a PASSED ✅
tests/test_errors.py::test_custom_exception_b PASSED ✅
```

## Задание 10.2 - Валидация данных и обработка ошибок валидации

### Реализовано:

1. **Модель Pydantic `UserData` с валидацией:**
   - `username`: строка, обязательное поле
   - `age`: целое число, **должно быть больше 18** (`gt=18`)
   - `email`: валидный email (`EmailStr`)
   - `password`: строка **от 8 до 16 символов** (`min_length=8, max_length=16`)
   - `phone`: опциональное поле, по умолчанию `"Unknown"`

2. **Эндпоинт `/register` (POST)** — принимает JSON с данными пользователя

3. **Кастомный обработчик `RequestValidationError`** — возвращает структурированный ответ с:
   - Полем `error`
   - Сообщением `message`
   - Детальным списком `details` (поле, причина ошибки, тип)
   - Исходным телом запроса `body`

### Примеры ответов:

**Успешная регистрация (200 OK):**
```json
{
  "message": "User john registered successfully",
  "data": {
    "username": "john",
    "age": 25,
    "email": "john@example.com",
    "password": "securepass123",
    "phone": "+1234567890"
  }
}
```

**Ошибка валидации (422 Unprocessable Entity):**
```json
{
  "error": "Validation error",
  "message": "Invalid input data",
  "details": [
    {
      "field": "body -> age",
      "message": "Input should be greater than 18",
      "type": "greater_than"
    }
  ],
  "body": {
    "username": "john",
    "age": 18,
    "email": "john@example.com",
    "password": "securepass123"
  }
}
```

### Тестирование:

```bash
# Ручная проверка
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john","age":25,"email":"john@example.com","password":"securepass123"}'

# Автотесты
PYTHONPATH=. pytest tests/test_validation.py -v
```

### Результат тестов:
```
tests/test_validation.py::test_register_user_success PASSED ✅
tests/test_validation.py::test_register_user_age_too_young PASSED ✅
tests/test_validation.py::test_register_user_invalid_email PASSED ✅
tests/test_validation.py::test_register_user_password_too_short PASSED ✅
tests/test_validation.py::test_register_user_password_too_long PASSED ✅
tests/test_validation.py::test_register_user_missing_required_field PASSED ✅
tests/test_validation.py::test_register_user_without_phone PASSED ✅
```

## Задание 11.1 - Модульные тесты для CRUD операций

### Реализовано:

1. **Три эндпоинта для работы с пользователями (in-memory хранилище):**
   - `POST /users` — создание пользователя (201 Created)
   - `GET /users/{id}` — получение пользователя по ID (200 OK)
   - `DELETE /users/{id}` — удаление пользователя (204 No Content)

2. **Модели Pydantic:**
   - `UserIn` — входные данные (username, age)
   - `UserOut` — выходные данные (id, username, age)

3. **Модульные тесты с pytest и TestClient:**
   - Успешное создание пользователя
   - Создание с отсутствующим обязательным полем (422)
   - Получение существующего пользователя
   - Получение несуществующего пользователя (404)
   - Успешное удаление пользователя
   - Удаление несуществующего пользователя (404)
   - Повторное удаление того же пользователя (404)

4. **Фикстура `clean_db`** — обеспечивает изоляцию состояния между тестами

### Примеры запросов:

```bash
# Создание пользователя
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"username":"john_doe","age":30}'

# Получение пользователя
curl http://localhost:8000/users/1

# Удаление пользователя
curl -X DELETE http://localhost:8000/users/1
```

### Тестирование:

```bash
# Запуск всех модульных тестов
PYTHONPATH=. pytest tests/test_unit.py -v

# Запуск конкретного теста
PYTHONPATH=. pytest tests/test_unit.py::TestUsersAPI::test_create_user_success -v
```

### Результат тестов:

```
tests/test_unit.py::TestUsersAPI::test_create_user_success PASSED ✅
tests/test_unit.py::TestUsersAPI::test_create_user_missing_field PASSED ✅
tests/test_unit.py::TestUsersAPI::test_get_user_success PASSED ✅
tests/test_unit.py::TestUsersAPI::test_get_user_not_found PASSED ✅
tests/test_unit.py::TestUsersAPI::test_delete_user_success PASSED ✅
tests/test_unit.py::TestUsersAPI::test_delete_user_not_found PASSED ✅
tests/test_unit.py::TestUsersAPI::test_delete_twice PASSED ✅
```

### Покрытые сценарии:

| Сценарий | Ожидаемый статус | Результат |
|----------|-----------------|-----------|
| Создание пользователя | 201 | ✅ |
| Создание без обязательного поля | 422 | ✅ |
| Получение существующего | 200 | ✅ |
| Получение несуществующего | 404 | ✅ |
| Удаление существующего | 204 | ✅ |
| Удаление несуществующего | 404 | ✅ |
| Повторное удаление | 404 | ✅ |

## Задание 11.2 - Асинхронные модульные тесты с Faker

### Реализовано:

1. **Асинхронные тесты** с использованием `pytest-asyncio`
2. **HTTP-клиент без запуска сервера** — `httpx.AsyncClient` с `ASGITransport`
3. **Генерация тестовых данных** через библиотеку **Faker**:
   - Случайные имена пользователей (`fake.user_name()`)
   - Случайный возраст (`fake.random_int(min=18, max=100)`)
4. **Изоляция состояния** — фикстура `clean_db` очищает in-memory БД между тестами
5. **Покрытые сценарии:**
   - Успешное создание пользователя
   - Получение существующего пользователя
   - Получение несуществующего пользователя (404)
   - Успешное удаление пользователя
   - Удаление несуществующего пользователя (404)
   - Повторное удаление того же пользователя (404)

### Технологии:

| Компонент | Назначение |
|-----------|------------|
| `pytest-asyncio` | Поддержка асинхронных тестов |
| `httpx.AsyncClient` | Асинхронные HTTP-запросы |
| `ASGITransport` | Напрямую вызывает приложение FastAPI |
| `Faker` | Генерация реалистичных тестовых данных |

### Тестирование:

```bash
# Запуск всех асинхронных тестов
PYTHONPATH=. pytest tests/test_async.py -v

# Запуск с подробным выводом
PYTHONPATH=. pytest tests/test_async.py -v --tb=short
```

### Результат тестов:

```
tests/test_async.py::TestAsyncUsersAPI::test_create_user_async PASSED ✅
tests/test_async.py::TestAsyncUsersAPI::test_get_user_success_async PASSED ✅
tests/test_async.py::TestAsyncUsersAPI::test_get_user_not_found_async PASSED ✅
tests/test_async.py::TestAsyncUsersAPI::test_delete_user_success_async PASSED ✅
tests/test_async.py::TestAsyncUsersAPI::test_delete_user_not_found_async PASSED ✅
tests/test_async.py::TestAsyncUsersAPI::test_delete_twice_async PASSED ✅
```

### Пример кода теста:

```python
async def test_create_user_async(self, async_client, clean_db):
    username = fake.user_name()
    age = fake.random_int(min=18, max=100)

    response = await async_client.post("/users", 
        json={"username": username, "age": age})
    
    assert response.status_code == 201
    assert response.json()["username"] == username
```

### Особенности реализации:

- **Фикстура `async_client`** — создаёт асинхронный клиент с `ASGITransport`, не требует запуска сервера
- **Фикстура `clean_db`** — очищает хранилище перед каждым тестом для изоляции
- **Декоратор `@pytest.mark.asyncio`** — указывает, что тест асинхронный