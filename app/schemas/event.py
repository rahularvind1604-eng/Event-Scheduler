from datetime import date
from pydantic import BaseModel, Field


class EventCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    location_city: str = Field(min_length=2, max_length=120)
    location_country: str = Field(min_length=2, max_length=120)
    timezone: str = Field(default="Europe/Madrid", min_length=2, max_length=64)
    start_date: date
    end_date: date


class EventOut(BaseModel):
    id: int
    company_id: int
    name: str
    location_city: str
    location_country: str
    timezone: str
    start_date: date
    end_date: date
    status: str

    class Config:
        from_attributes = True
