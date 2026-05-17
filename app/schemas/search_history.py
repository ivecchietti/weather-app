from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SearchHistoryResponse(BaseModel):
    id: int
    query: str
    weather_record_id: int | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )