from sqlalchemy.orm import Session
from app.core.errors import ConflictError, NotFoundError, ValidationError
from app.repositories.company_repo import CompanyRepository
from app.repositories.user_repo import UserRepository

ALLOWED_ROLES = {"admin", "organizer", "attendee"}


class UserService:
    def __init__(self, db: Session):
        self.company_repo = CompanyRepository(db)
        self.user_repo = UserRepository(db)

    def create_user(self, company_id: int, name: str, email: str, role: str):
        company = self.company_repo.get_by_id(company_id)
        if not company:
            raise NotFoundError("Company not found.")

        if role not in ALLOWED_ROLES:
            raise ValidationError(f"Invalid role '{role}'. Must be one of {sorted(ALLOWED_ROLES)}.")

        if self.user_repo.get_by_email_in_company(company_id, email):
            raise ConflictError("A user with this email already exists in this company.")

        return self.user_repo.create(company_id=company_id, name=name, email=email, role=role)
