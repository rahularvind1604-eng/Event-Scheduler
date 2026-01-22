from sqlalchemy.orm import Session
from app.db.models import Event


class EventRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, event_id: int) -> Event | None:
        return self.db.query(Event).filter(Event.id == event_id).first()

    def create(
        self,
        company_id: int,
        name: str,
        location_city: str,
        location_country: str,
        timezone: str,
        start_date,
        end_date,
    ) -> Event:
        event = Event(
            company_id=company_id,
            name=name,
            location_city=location_city,
            location_country=location_country,
            timezone=timezone,
            start_date=start_date,
            end_date=end_date,
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event
