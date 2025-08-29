from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from app.core.models.base import BaseModel


class Rule(BaseModel):
    org_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    name = Column(String, nullable=False)
    definition = Column(Text, nullable=False)  # JSON string of rule definition
    enabled = Column(Boolean, default=True)
    priority = Column(Integer, default=1)
    category = Column(String, default="general")  # sales, finance, support, etc.
    
    # Relationships
    organization = relationship("Organization", back_populates="rules")
