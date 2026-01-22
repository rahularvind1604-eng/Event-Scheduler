from sqlalchemy.orm import Session
from app.db.models import User

class UserRepository:
    def __init__(self, db:Session):
        self.db=db
    
    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email_in_company(self, company_id: int, email: str) -> User | None:
        return (
            self.db.query(User)
            .filter(User.company_id == company_id, User.email == email)
            .first()
        )

    def create(self, company_id: int, name: str, email: str, role: str) -> User:
        user = User(company_id=company_id, name=name, email=email, role=role)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
