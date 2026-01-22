from sqlalchemy.orm import Session
from app.core.errors import ConflictError
from app.repositories.company_repo import CompanyRepository


class CompanyService:
    def __init__(self, db: Session):
        self.repo = CompanyRepository(db)

    def create_company(self, name: str):
        if self.repo.get_by_name(name):
            raise ConflictError(f"Company '{name}' already exists.")
        return self.repo.create(name=name)
