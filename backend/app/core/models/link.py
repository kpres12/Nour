from sqlalchemy import Column, String, Integer, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from app.core.models.base import BaseModel


class Link(BaseModel):
    org_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    src_entity_id = Column(Integer, ForeignKey("entity.id"), nullable=False)
    dst_entity_id = Column(Integer, ForeignKey("entity.id"), nullable=False)
    type = Column(String, nullable=False)  # owns, works_for, has_deal, etc.
    properties = Column(Text, default="{}")  # JSON string of link properties
    confidence = Column(Float, default=1.0)  # confidence score for link
    
    # Relationships
    organization = relationship("Organization", back_populates="links")
    source_entity = relationship("Entity", foreign_keys=[src_entity_id], back_populates="source_links")
    target_entity = relationship("Entity", foreign_keys=[dst_entity_id], back_populates="target_links")
