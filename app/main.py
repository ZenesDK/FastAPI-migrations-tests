from fastapi import FastAPI
from app.database import engine, Base

# Создание таблиц (не для миграций, а для проверки)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="KR4 API")


@app.get("/")
def root():
    return {"message": "KR4 API", "status": "ok"}