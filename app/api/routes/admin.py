from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.errors import AppError, ConflictError, NotFoundError, ValidationError
from app.db.session import get_db
from app.schemas.company import CompanyCreate, CompanyOut
from app.schemas.user import UserCreate, UserOut
from app.schemas.event import EventCreate, EventOut
from app.schemas.room import RoomsConfigRequest, EventRoomOut
from app.services.company_service import CompanyService
from app.services.user_service import UserService
from app.services.event_service import EventService
from app.services.room_service import RoomService

router = APIRouter(prefix="/admin", tags=["Admin"])


def _raise_http(err: AppError) -> None:
    if isinstance(err, NotFoundError):
        raise HTTPException(status_code=404, detail={"error_code": err.error_code, "message": err.message})
    if isinstance(err, ConflictError):
        raise HTTPException(status_code=409, detail={"error_code": err.error_code, "message": err.message})
    if isinstance(err, ValidationError):
        raise HTTPException(status_code=400, detail={"error_code": err.error_code, "message": err.message})
    raise HTTPException(status_code=500, detail={"error_code": err.error_code, "message": err.message})


@router.post("/companies", response_model=CompanyOut, status_code=status.HTTP_201_CREATED)
def create_company(payload: CompanyCreate, db: Session = Depends(get_db)):
    try:
        return CompanyService(db).create_company(name=payload.name)
    except AppError as e:
        _raise_http(e)


@router.post("/companies/{company_id}/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(company_id: int, payload: UserCreate, db: Session = Depends(get_db)):
    try:
        return UserService(db).create_user(
            company_id=company_id,
            name=payload.name,
            email=str(payload.email),
            role=payload.role,
        )
    except AppError as e:
        _raise_http(e)


@router.post("/companies/{company_id}/events", response_model=EventOut, status_code=status.HTTP_201_CREATED)
def create_event(company_id: int, payload: EventCreate, db: Session = Depends(get_db)):
    try:
        return EventService(db).create_event(
            company_id=company_id,
            name=payload.name,
            location_city=payload.location_city,
            location_country=payload.location_country,
            timezone=payload.timezone,
            start_date=payload.start_date,
            end_date=payload.end_date,
        )
    except AppError as e:
        _raise_http(e)


@router.post("/events/{event_id}/rooms", response_model=list[EventRoomOut], status_code=status.HTTP_201_CREATED)
def configure_rooms(event_id: int, payload: RoomsConfigRequest, db: Session = Depends(get_db)):
    try:
        return RoomService(db).configure_rooms(
            event_id=event_id,
            room_count=payload.room_count,
            default_locations=payload.default_locations,
        )
    except AppError as e:
        _raise_http(e)
