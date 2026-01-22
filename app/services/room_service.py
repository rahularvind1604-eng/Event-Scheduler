from sqlalchemy.orm import Session
from app.core.errors import ConflictError, NotFoundError, ValidationError
from app.db.models import EventRoom
from app.repositories.event_repo import EventRepository
from app.repositories.room_repo import EventRoomRepository


class RoomService:
    def __init__(self, db: Session):
        self.event_repo = EventRepository(db)
        self.room_repo = EventRoomRepository(db)

    def configure_rooms(self, event_id: int, room_count: int, default_locations: list[str] | None):
        event = self.event_repo.get_by_id(event_id)
        if not event:
            raise NotFoundError("Event not found.")

        if self.room_repo.has_any_rooms(event_id):
            raise ConflictError("Rooms are already configured for this event.")

        if default_locations is not None and len(default_locations) != room_count:
            raise ValidationError("default_locations length must match room_count.")

        rooms: list[EventRoom] = []

        # Create Room 1..N
        for i in range(1, room_count + 1):
            loc = default_locations[i - 1] if default_locations else None
            rooms.append(
                EventRoom(
                    event_id=event_id,
                    name=f"Room {i}",
                    default_location=loc,
                    is_other=False,
                )
            )

        # Always add "Other"
        rooms.append(
            EventRoom(
                event_id=event_id,
                name="Other",
                default_location=None,
                is_other=True,
            )
        )

        return self.room_repo.create_many(rooms)
