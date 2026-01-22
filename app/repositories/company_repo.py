from sqlalchemy.orm import Session
from app.db.models import Company

class CompanyRepository:
    def __init__(self, db:Session):
        self.db=db
    
    def get_by_id(self,company_id:int)-> Company | None:
        return self.db.query(Company).filter(Company.id==company_id).first()
    
    def get_by_name(self,company_name:str)->Company | None:
        return self.db.query(Company).filter(Company.name==name).first()
    
    def create(self, name:str)->Company:
        company=Company(name=name)
        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)
        return company