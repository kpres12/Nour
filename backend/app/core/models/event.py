from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.core.models.base import BaseModel


class Event(BaseModel):
    org_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    entity_id = Column(Integer, ForeignKey("entity.id"), nullable=False)
    type = Column(String, nullable=False)  # purchase, payment, ticket, meeting, etc.
    timestamp = Column(DateTime, nullable=False)
    properties = Column(Text, default="{}")  # JSON string of event properties
    
    # Relationships
    organization = relationship("Organization", back_populates="events")
    entity = relationship("Entity", back_populates="events")
