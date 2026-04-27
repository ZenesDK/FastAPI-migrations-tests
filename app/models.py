from sqlalchemy import Column, Integer, String, Float
from app.database import Base
from pydantic import BaseModel, EmailStr, conint, constr
from typing import Optional


class UserData(BaseModel):
    username: str
    age: conint(gt=18)  # type: ignore - возраст должен быть больше 18
    email: EmailStr
    password: constr(min_length=8, max_length=16)  # type: ignore
    phone: Optional[str] = "Unknown"


class ErrorResponse(BaseModel):
    status_code: int
    error: str
    message: str


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    count = Column(Integer, nullable=False)
    # description добавим позже во второй миграции

class UserIn(BaseModel):
    username: str
    age: int


class UserOut(BaseModel):
    id: int
    username: str
    age: int