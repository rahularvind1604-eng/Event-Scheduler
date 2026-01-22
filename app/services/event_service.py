from datetime import timedelta
from sqlalchemy.orm import Session
from app.core.errors import NotFoundError, ValidationError
from app.repositories.company_repo import CompanyRepository
from app.repositories.event_repo import EventRepository


class EventService:
    def __init__(self, db: Session):
        self.company_repo = CompanyRepository(db)
        self.event_repo = EventRepository(db)

    def create_event(
        self,
        company_id: int,
        name: str,
        location_city: str,
        location_country: str,
        timezone: str,
        start_date,
        end_date,
    ):
        company = self.company_repo.get_by_id(company_id)
        if not company:
            raise NotFoundError("Company not found.")

        # V1 rule: event must be exactly 3 days (start + 2)
        expected_end = start_date + timedelta(days=2)
        if end_date != expected_end:
            raise ValidationError("Event must span exactly 3 days (end_date must be start_date + 2 days).")

        return self.event_repo.create(
            company_id=company_id,
            name=name,
            location_city=location_city,
            location_country=location_country,
            timezone=timezone,
            start_date=start_date,
            end_date=end_date,
        )
