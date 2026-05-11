from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Weather App Backend"
    weather_api_key: str
    database_url: str
    api_key: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()