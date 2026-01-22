"""
Database models for EventPilot.

These models define the core domain entities:
- Company (client / tenant)
- User (admin / organizer / attendee)
- Event (3-day conference or exhibition)
- EventRoom (rooms available per event)

Design principles:
- Explicit relationships
- Clear ownership boundaries
- Database-level constraints for data integrity
"""

from datetime import date

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Company(Base):
    """
    Represents a client (tenant) using the system.
    Example: Samsung, Google, Amazon.

    A company owns:
    - users
    - events
    """

    __tablename__ = "companies"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Company name must be unique across the system
    name = Column(String(200), nullable=False, unique=True, index=True)

    # One-to-many relationships
    users = relationship(
        "User",
        back_populates="company",
        cascade="all, delete-orphan",
    )
    events = relationship(
        "Event",
        back_populates="company",
        cascade="all, delete-orphan",
    )


class User(Base):
    """
    Represents a user belonging to a company.

    Roles:
    - admin: manages companies, events, rooms
    - organizer: schedules and manages meetings
    - attendee: participates in meetings

    Email is unique per company (multi-tenant safe).
    """

    __tablename__ = "users"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Foreign key to owning company
    company_id = Column(
        Integer,
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # User details
    name = Column(String(200), nullable=False)
    email = Column(String(255), nullable=False)

    # Role-based access control (RBAC)
    role = Column(
        String(50),
        nullable=False,
        default="attendee",  # admin | organizer | attendee
    )

    # Soft flag to deactivate users without deleting data
    active = Column(Boolean, nullable=False, default=True)

    # Relationship back to company
    company = relationship("Company", back_populates="users")

    # Ensure email uniqueness within the same company
    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "email",
            name="uq_users_company_email",
        ),
    )


class Event(Base):
    """
    Represents an event (e.g., MWC Barcelona).

    Event characteristics:
    - Always spans exactly 3 days in V1
    - Owned by a company
    - Contains multiple rooms
    """

    __tablename__ = "events"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Owning company
    company_id = Column(
        Integer,
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Event metadata
    name = Column(String(200), nullable=False)
    location_city = Column(String(120), nullable=False)
    location_country = Column(String(120), nullable=False)

    # Timezone used for all meetings in this event
    timezone = Column(String(64), nullable=False, default="Europe/Madrid")

    # Event date range (must be exactly 3 days; enforced at service layer)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    # Event lifecycle status
    status = Column(
        String(30),
        nullable=False,
        default="active",  # active | canceled | archived
    )

    # Relationships
    company = relationship("Company", back_populates="events")
    rooms = relationship(
        "EventRoom",
        back_populates="event",
        cascade="all, delete-orphan",
    )

    # Basic data integrity check
    __table_args__ = (
        CheckConstraint(
            "end_date >= start_date",
            name="ck_event_date_range",
        ),
    )


class EventRoom(Base):
    """
    Represents a room available within an event.

    Room types:
    - Standard rooms (Room 1, Room 2, ...)
    - Special 'Other' room with custom location per meeting

    A room name must be unique within an event.
    """

    __tablename__ = "event_rooms"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Owning event
    event_id = Column(
        Integer,
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Human-readable room name (e.g., "Room 1", "Other")
    name = Column(String(100), nullable=False)

    # Default physical location for the room
    # (null for "Other" rooms)
    default_location = Column(String(255), nullable=True)

    # Flag to identify the special "Other" room
    is_other = Column(Boolean, nullable=False, default=False)

    # Relationship back to event
    event = relationship("Event", back_populates="rooms")

    # Ensure room names are unique per event
    __table_args__ = (
        UniqueConstraint(
            "event_id",
            "name",
            name="uq_event_rooms_event_name",
        ),
    )
