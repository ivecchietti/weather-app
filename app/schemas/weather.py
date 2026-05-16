from datetime import datetime

from pydantic import BaseModel


class WeatherSearchRequest(BaseModel):
    location: str


class WeatherRecordUpdate(BaseModel):
    location_query: str | None = None
    resolved_location: str | None = None


class WeatherRecordResponse(BaseModel):
    id: int
    user_id: int | None
    location_query: str
    resolved_location: str | None
    temperature: float | None
    feels_like: float | None
    humidity: int | None
    weather_main: str | None
    weather_description: str | None
    wind_speed: float | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }