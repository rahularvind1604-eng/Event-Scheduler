from pydantic import BaseModel, EmailStr, Field
from typing import Literal

UserRole=Literal["admin","organizer","attendee"]

class UserCreate(BaseModel):
    name: str = Field(min_length=2,max_length=200)
    email:EmailStr
    role: UserRole

class UserOut(BaseModel):
    id:int
    company_id:id
    name: str
    role:str
    active:bool

    def Config:
        from_attributes=True
        