from sqlalchemy import Column, String, Boolean
from app.core.models.base import BaseModel


class Organization(BaseModel):
    name = Column(String, unique=True, index=True, nullable=False)
    domain = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    settings = Column(String, default="{}")  # JSON string for org-specific settings
