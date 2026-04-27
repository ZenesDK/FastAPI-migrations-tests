from fastapi import FastAPI
from app.exceptions import register_exception_handlers, CustomExceptionA, CustomExceptionB
from app.database import engine, Base
from app.models import UserData
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.routers import users

# Создание таблиц (для 9.1)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="KR4 API")

app.include_router(users.router)

# Регистрация обработчиков исключений (задание 10.1)
register_exception_handlers(app)


# Эндпоинты для задания 10.1
@app.get("/forbidden")
async def trigger_forbidden():
    """Вызывает CustomExceptionA (403 Forbidden)"""
    raise CustomExceptionA(detail="Access denied: insufficient permissions")


@app.get("/not-found")
async def trigger_not_found():
    """Вызывает CustomExceptionB (404 Not Found)"""
    raise CustomExceptionB(detail="The requested resource does not exist")


@app.get("/")
async def root():
    return {"message": "KR4 API", "status": "ok"}

@app.post("/register")
async def register_user(user: UserData):
    """Регистрация пользователя с валидацией"""
    return {"message": f"User {user.username} registered successfully", "data": user.model_dump()}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    formatted_errors = []
    for err in exc.errors():
        formatted_errors.append({
            "field": " -> ".join(str(loc) for loc in err["loc"]),
            "message": err["msg"],
            "type": err["type"]
        })

    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "message": "Invalid input data",
            "details": formatted_errors,
            "body": exc.body
        }
    )