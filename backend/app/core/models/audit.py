from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.models.base import BaseModel


class AuditLog(BaseModel):
    org_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    actor_id = Column(Integer, ForeignKey("entity.id"), nullable=True)  # user who performed action
    action = Column(String, nullable=False)  # create, read, update, delete, etc.
    resource_type = Column(String, nullable=False)  # entity, narrative, signal, etc.
    resource_id = Column(Integer, nullable=True)  # ID of affected resource
    metadata = Column(Text, default="{}")  # JSON string of additional context
    
    # Relationships
    organization = relationship("Organization", back_populates="audit_logs")
    actor = relationship("Entity", back_populates="audit_actions")
