from pydantic import BaseModel, Field
from typing import List, Optional


class RoomsConfigRequest(BaseModel):
    room_count: int = Field(ge=1, le=20)
    # Optional: if provided, length must equal room_count
    default_locations: Optional[List[str]] = None


class EventRoomOut(BaseModel):
    id: int
    event_id: int
    name: str
    default_location: Optional[str]
    is_other: bool

    class Config:
        from_attributes = True
