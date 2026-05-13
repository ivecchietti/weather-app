from fastapi import FastAPI

from app.api.routes import auth, users, weather
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)

app.include_router(weather.router)
app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": f"{settings.app_name} is running"}