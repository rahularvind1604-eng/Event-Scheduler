from pydantic import BaseModel, Field

class CompanyCreate(BaseModel):
    name: str - Field(min_length=2, mas_length=200)

class COmpanyOut(BaseModel):
    id:int
    name: str

    class config:
        from_attributes=True