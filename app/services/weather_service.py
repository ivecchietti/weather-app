import requests

from app.core.config import settings

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_current_weather(location: str) -> dict:
    params = {
        "q": location,
        "appid": settings.weather_api_key,
        "units": "metric",
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()