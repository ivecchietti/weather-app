from fastapi import FastAPI

from app.api.routes import weather
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)

app.include_router(weather.router)


@app.get("/")
def root():
    return {"message": f"{settings.app_name} is running"}