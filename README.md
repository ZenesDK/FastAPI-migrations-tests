# Контрольная работа №4 - FastAPI

## 📌 Описание

Контрольная работа №4 по дисциплине «Технологии разработки серверных приложений» включает реализацию следующих тем:

- **Миграции баз данных** с использованием Alembic и SQLAlchemy
- **Кастомная обработка ошибок** и исключений
- **Валидация данных** с помощью Pydantic
- **Модульное тестирование** (синхронное и асинхронное) с pytest
- **Генерация тестовых данных** с помощью Faker

---

## 🚀 Быстрый старт

### Требования

- Python 3.10 или выше
- pip (менеджер пакетов)
- SQLite (встроен в Python)

### Установка и запуск

```bash
# 1. Клонирование репозитория
git clone https://github.com/ZenesDK/FastAPI-migrations-tests
cd FastAPI-migrations-tests

# 2. Создание и активация виртуального окружения
python -m venv venv
source venv/bin/activate      # Linux/Mac
# или
venv\Scripts\activate         # Windows

# 3. Установка зависимостей
pip install -r requirements.txt

# 4. Настройка переменных окружения
cp .env.example .env
# (опционально) отредактируйте .env при необходимости

# 5. Применение миграций базы данных
alembic upgrade head

# 6. Запуск приложения
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу: **http://localhost:8000**

---

## 📚 Структура проекта

```
FastAPI-migrations-tests/
├── app/                      # Основной код приложения
│   ├── __init__.py
│   ├── main.py               # FastAPI приложение
│   ├── models.py             # Pydantic и SQLAlchemy модели
│   ├── database.py           # Подключение к БД
│   ├── exceptions.py         # Кастомные исключения
│   └── routers/
│       ├── __init__.py
│       └── users.py          # CRUD эндпоинты
├── tests/                    # Тесты
│   ├── __init__.py
│   ├── conftest.py           # Фикстуры pytest
│   ├── test_errors.py        # Тесты 10.1
│   ├── test_validation.py    # Тесты 10.2
│   ├── test_unit.py          # Тесты 11.1
│   └── test_async.py         # Тесты 11.2
├── alembic/                  # Миграции Alembic
├── alembic.ini               # Конфигурация Alembic
├── requirements.txt          # Зависимости
├── .env.example              # Пример переменных окружения
├── .gitignore                # Игнорируемые файлы
└── README.md                 # Этот файл
```

---

## 🔧 Переменные окружения

Создайте файл `.env` на основе `.env.example`:

```env
DATABASE_URL=sqlite:///./test.db
```

---

## 🧪 Как проверить работоспособность

### 1. Запуск всех тестов

```bash
# Убедитесь, что виртуальное окружение активировано
source venv/bin/activate  # Linux/Mac

# Запуск всех тестов
PYTHONPATH=. pytest tests/ -v

# Запуск с отчётом о покрытии (если установлен pytest-cov)
PYTHONPATH=. pytest tests/ -v --cov=app
```

### 2. Проверка через API (curl)

```bash
# Корневой эндпоинт
curl http://localhost:8000/

# 10.1 - Кастомные исключения
curl http://localhost:8000/forbidden
curl http://localhost:8000/not-found

# 10.2 - Регистрация с валидацией
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john","age":25,"email":"john@example.com","password":"securepass123"}'

# 11.1 - CRUD операции с пользователями
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","age":30}'

curl http://localhost:8000/users/1

curl -X DELETE http://localhost:8000/users/1
```

### 3. Проверка через Swagger документацию

Открой в браузере: **http://localhost:8000/docs**

---

## 📋 Проверка заданий по отдельности

### Задание 9.1 - Миграции Alembic

```bash
# Проверить текущую версию миграций
alembic current

# Посмотреть историю миграций
alembic history

# Проверить, что таблица products создана
sqlite3 test.db "SELECT * FROM products;"
```

**Ожидаемый результат:** Таблица `products` существует, содержит поля `id`, `title`, `price`, `count`, `description`.

### Задание 10.1 - Кастомная обработка ошибок

```bash
# Должен вернуть 403 с кастомным сообщением
curl -v http://localhost:8000/forbidden

# Должен вернуть 404 с кастомным сообщением
curl -v http://localhost:8000/not-found

# Запуск тестов
PYTHONPATH=. pytest tests/test_errors.py -v
```

### Задание 10.2 - Валидация данных

```bash
# Успешная регистрация
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"valid_user","age":25,"email":"user@example.com","password":"securepass123"}'

# Ошибка: возраст <= 18
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"young","age":18,"email":"young@example.com","password":"securepass123"}'

# Ошибка: невалидный email
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"bad_email","age":25,"email":"not-an-email","password":"securepass123"}'

# Запуск тестов
PYTHONPATH=. pytest tests/test_validation.py -v
```

### Задание 11.1 - Модульные тесты для CRUD

```bash
# Создание пользователя
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","age":25}'

# Получение пользователя
curl http://localhost:8000/users/1

# Удаление пользователя
curl -X DELETE http://localhost:8000/users/1

# Попытка получить удалённого пользователя (404)
curl http://localhost:8000/users/1

# Запуск тестов
PYTHONPATH=. pytest tests/test_unit.py -v
```

### Задание 11.2 - Асинхронные тесты с Faker

```bash
# Запуск асинхронных тестов
PYTHONPATH=. pytest tests/test_async.py -v
```

---

## 📊 Результаты тестов

### test_errors.py (6 тестов)
```
tests/test_errors.py::test_custom_exception_a PASSED ✅
tests/test_errors.py::test_custom_exception_b PASSED ✅
```

### test_validation.py (7 тестов)
```
tests/test_validation.py::test_register_user_success PASSED ✅
tests/test_validation.py::test_register_user_age_too_young PASSED ✅
tests/test_validation.py::test_register_user_invalid_email PASSED ✅
tests/test_validation.py::test_register_user_password_too_short PASSED ✅
tests/test_validation.py::test_register_user_password_too_long PASSED ✅
tests/test_validation.py::test_register_user_missing_required_field PASSED ✅
tests/test_validation.py::test_register_user_without_phone PASSED ✅
```

### test_unit.py (7 тестов)
```
tests/test_unit.py::TestUsersAPI::test_create_user_success PASSED ✅
tests/test_unit.py::TestUsersAPI::test_create_user_missing_field PASSED ✅
tests/test_unit.py::TestUsersAPI::test_get_user_success PASSED ✅
tests/test_unit.py::TestUsersAPI::test_get_user_not_found PASSED ✅
tests/test_unit.py::TestUsersAPI::test_delete_user_success PASSED ✅
tests/test_unit.py::TestUsersAPI::test_delete_user_not_found PASSED ✅
tests/test_unit.py::TestUsersAPI::test_delete_twice PASSED ✅
```

### test_async.py (6 тестов)
```
tests/test_async.py::TestAsyncUsersAPI::test_create_user_async PASSED ✅
tests/test_async.py::TestAsyncUsersAPI::test_get_user_success_async PASSED ✅
tests/test_async.py::TestAsyncUsersAPI::test_get_user_not_found_async PASSED ✅
tests/test_async.py::TestAsyncUsersAPI::test_delete_user_success_async PASSED ✅
tests/test_async.py::TestAsyncUsersAPI::test_delete_user_not_found_async PASSED ✅
tests/test_async.py::TestAsyncUsersAPI::test_delete_twice_async PASSED ✅
```

**Всего тестов:** 22  
**Пройдено:** 22 ✅  
**Провалено:** 0 ❌

---

## 🛠️ Устранение неполадок

### Ошибка: `ModuleNotFoundError: No module named 'app'`

```bash
# Используйте PYTHONPATH при запуске тестов
PYTHONPATH=. pytest tests/ -v
```

### Ошибка: `email-validator is not installed`

```bash
pip install email-validator
```

### Ошибка при миграции: `Cannot add a NOT NULL column with default value NULL`

В файле миграции добавьте `server_default=''`:

```python
op.add_column('products', sa.Column('description', sa.String(), nullable=False, server_default=''))
```

### Ошибка: `pytest: command not found`

```bash
# Активируйте виртуальное окружение
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установите pytest
pip install pytest pytest-asyncio httpx Faker
```

---

## 📝 Выполненные задания

| Задание | Описание | Статус |
|---------|----------|--------|
| 9.1 | Миграции Alembic (создание и обновление таблицы Product) | ✅ |
| 10.1 | Кастомные исключения и обработчики ошибок | ✅ |
| 10.2 | Валидация данных и обработка RequestValidationError | ✅ |
| 11.1 | Модульные тесты для CRUD операций | ✅ |
| 11.2 | Асинхронные тесты с Faker и httpx | ✅ |

---