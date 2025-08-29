from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from app.core.models.base import BaseModel


class Narrative(BaseModel):
    org_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    evidence = Column(Text, default="{}")  # JSON string of supporting evidence
    actions = Column(Text, default="[]")  # JSON string of action recommendations
    generated_at = Column(DateTime, nullable=False)
    author = Column(String, default="ai")  # ai or analyst
    status = Column(String, default="active")  # active, archived, dismissed
    
    # Relationships
    organization = relationship("Organization", back_populates="narratives")
