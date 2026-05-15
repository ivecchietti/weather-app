from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.search_history import SearchHistory
from app.models.user import User
from app.models.weather_record import WeatherRecord
from app.schemas.search_history import SearchHistoryResponse
from app.schemas.weather import (
    WeatherRecordResponse,
    WeatherSearchRequest,
)
from app.services.weather_service import fetch_current_weather

router = APIRouter(prefix="/weather", tags=["weather"])


@router.post(
    "/current",
    response_model=WeatherRecordResponse,
)
def get_current_weather(
    request: WeatherSearchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        weather_data = fetch_current_weather(
            request.location
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch weather data",
        )

    weather_record = WeatherRecord(
        user_id=current_user.id,
        location_query=request.location,
        resolved_location=weather_data["name"],
        temperature=weather_data["main"]["temp"],
        feels_like=weather_data["main"]["feels_like"],
        humidity=weather_data["main"]["humidity"],
        weather_main=weather_data["weather"][0]["main"],
        weather_description=weather_data["weather"][0]["description"],
        wind_speed=weather_data["wind"]["speed"],
    )

    db.add(weather_record)
    db.commit()
    db.refresh(weather_record)

    search_history = SearchHistory(
        user_id=current_user.id,
        weather_record_id=weather_record.id,
        query=request.location,
    )

    db.add(search_history)
    db.commit()

    return weather_record


@router.get(
    "/history",
    response_model=list[SearchHistoryResponse],
)
def get_search_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    history = (
        db.query(SearchHistory)
        .filter(SearchHistory.user_id == current_user.id)
        .order_by(SearchHistory.created_at.desc())
        .limit(10)
        .all()
    )

    return history