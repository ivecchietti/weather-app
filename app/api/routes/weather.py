import csv
from io import StringIO

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.search_history import SearchHistory
from app.models.user import User
from app.models.weather_record import WeatherRecord
from app.schemas.search_history import SearchHistoryResponse
from app.schemas.weather import (
    ForecastItem,
    ForecastResponse,
    WeatherRecordResponse,
    WeatherRecordUpdate,
    WeatherSearchRequest,
)
from app.services.weather_service import (
    fetch_current_weather,
    fetch_weather_forecast,
)

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
        weather_data = fetch_current_weather(request.location)
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


@router.post(
    "/forecast",
    response_model=ForecastResponse,
)
def get_weather_forecast(
    request: WeatherSearchRequest,
):
    try:
        forecast_data = fetch_weather_forecast(
            request.location
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch forecast data",
        )

    daily_forecasts = []

    for item in forecast_data["list"]:
        if "12:00:00" in item["dt_txt"]:
            daily_forecasts.append(
                ForecastItem(
                    date=item["dt_txt"].split(" ")[0],
                    temperature=item["main"]["temp"],
                    humidity=item["main"]["humidity"],
                    description=item["weather"][0]["description"],
                )
            )

    return ForecastResponse(
        location=forecast_data["city"]["name"],
        forecast=daily_forecasts[:5],
    )


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


@router.get(
    "/records",
    response_model=list[WeatherRecordResponse],
)
def get_weather_records(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    records = (
        db.query(WeatherRecord)
        .filter(WeatherRecord.user_id == current_user.id)
        .order_by(WeatherRecord.created_at.desc())
        .all()
    )

    return records


@router.get("/export/csv")
def export_weather_records_csv(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    records = (
        db.query(WeatherRecord)
        .filter(WeatherRecord.user_id == current_user.id)
        .order_by(WeatherRecord.created_at.desc())
        .all()
    )

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(
        [
            "id",
            "location_query",
            "resolved_location",
            "temperature",
            "feels_like",
            "humidity",
            "weather_main",
            "weather_description",
            "wind_speed",
            "created_at",
        ]
    )

    for record in records:
        writer.writerow(
            [
                record.id,
                record.location_query,
                record.resolved_location,
                record.temperature,
                record.feels_like,
                record.humidity,
                record.weather_main,
                record.weather_description,
                record.wind_speed,
                record.created_at,
            ]
        )

    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": (
                "attachment; filename=weather_records.csv"
            )
        },
    )


@router.get(
    "/{weather_id}",
    response_model=WeatherRecordResponse,
)
def get_weather_record(
    weather_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    weather_record = (
        db.query(WeatherRecord)
        .filter(
            WeatherRecord.id == weather_id,
            WeatherRecord.user_id == current_user.id,
        )
        .first()
    )

    if not weather_record:
        raise HTTPException(
            status_code=404,
            detail="Weather record not found",
        )

    return weather_record


@router.put(
    "/{weather_id}",
    response_model=WeatherRecordResponse,
)
def update_weather_record(
    weather_id: int,
    request: WeatherRecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    weather_record = (
        db.query(WeatherRecord)
        .filter(
            WeatherRecord.id == weather_id,
            WeatherRecord.user_id == current_user.id,
        )
        .first()
    )

    if not weather_record:
        raise HTTPException(
            status_code=404,
            detail="Weather record not found",
        )

    if request.location_query is not None:
        weather_record.location_query = request.location_query

    if request.resolved_location is not None:
        weather_record.resolved_location = request.resolved_location

    db.commit()
    db.refresh(weather_record)

    return weather_record


@router.delete(
    "/{weather_id}",
)
def delete_weather_record(
    weather_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    weather_record = (
        db.query(WeatherRecord)
        .filter(
            WeatherRecord.id == weather_id,
            WeatherRecord.user_id == current_user.id,
        )
        .first()
    )

    if not weather_record:
        raise HTTPException(
            status_code=404,
            detail="Weather record not found",
        )

    db.delete(weather_record)
    db.commit()

    return {
        "message": "Weather record deleted successfully"
    }