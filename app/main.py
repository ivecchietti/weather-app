from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import (
    HTTPException as StarletteHTTPException,
)

from app.api.routes import auth, users, weather
from app.core.config import settings
from app.exceptions.handlers import (
    generic_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)

app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    Exception,
    generic_exception_handler,
)

app.include_router(weather.router)
app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {
        "message": f"{settings.app_name} is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }