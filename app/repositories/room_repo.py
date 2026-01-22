from sqlalchemy.orm import Session
from app.db.models import EventRoom


class EventRoomRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_event(self, event_id: int) -> list[EventRoom]:
        return self.db.query(EventRoom).filter(EventRoom.event_id == event_id).all()

    def has_any_rooms(self, event_id: int) -> bool:
        return (
            self.db.query(EventRoom.id)
            .filter(EventRoom.event_id == event_id)
            .first()
            is not None
        )

    def create_many(self, rooms: list[EventRoom]) -> list[EventRoom]:
        self.db.add_all(rooms)
        self.db.commit()
        for r in rooms:
            self.db.refresh(r)
        return rooms
