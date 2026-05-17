import requests

from app.core.config import settings

CURRENT_WEATHER_URL = (
    "https://api.openweathermap.org/data/2.5/weather"
)

FORECAST_URL = (
    "https://api.openweathermap.org/data/2.5/forecast"
)


def fetch_current_weather(location: str) -> dict:
    params = {
        "q": location,
        "appid": settings.weather_api_key,
        "units": "metric",
    }

    response = requests.get(
        CURRENT_WEATHER_URL,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


def fetch_weather_forecast(location: str) -> dict:
    params = {
        "q": location,
        "appid": settings.weather_api_key,
        "units": "metric",
    }

    response = requests.get(
        FORECAST_URL,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()