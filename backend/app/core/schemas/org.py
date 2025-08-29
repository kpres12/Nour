from pydantic import BaseModel
from typing import Optional


class OrganizationCreate(BaseModel):
    name: str
    domain: Optional[str] = None


class OrganizationResponse(BaseModel):
    id: int
    name: str
    domain: Optional[str] = None
    is_active: bool
    
    class Config:
        from_attributes = True
