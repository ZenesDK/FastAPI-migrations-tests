from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.models import ErrorResponse


# Кастомные исключения
class CustomExceptionA(HTTPException):
    def __init__(self, detail: str = "Resource forbidden", status_code: int = 403):
        super().__init__(status_code=status_code, detail=detail)
        self.message = detail


class CustomExceptionB(HTTPException):
    def __init__(self, detail: str = "Resource not found", status_code: int = 404):
        super().__init__(status_code=status_code, detail=detail)
        self.message = detail


# Регистрация обработчиков
def register_exception_handlers(app):
    @app.exception_handler(CustomExceptionA)
    async def custom_exception_a_handler(request: Request, exc: CustomExceptionA):
        error_response = ErrorResponse(
            status_code=exc.status_code,
            error="ForbiddenError",
            message=exc.message
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=jsonable_encoder(error_response)
        )

    @app.exception_handler(CustomExceptionB)
    async def custom_exception_b_handler(request: Request, exc: CustomExceptionB):
        error_response = ErrorResponse(
            status_code=exc.status_code,
            error="NotFoundError",
            message=exc.message
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=jsonable_encoder(error_response)
        )