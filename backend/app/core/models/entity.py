from sqlalchemy import Column, String, Integer, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from app.core.models.base import BaseModel


class Entity(BaseModel):
    org_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    type = Column(String, nullable=False)  # person, company, deal, invoice, etc.
    canonical = Column(Text, nullable=False)  # JSON string of canonical data
    confidence = Column(Float, default=1.0)  # confidence score for resolution
    provenance = Column(Text, default="{}")  # JSON string of source data
    external_id = Column(String, index=True)  # external system ID if available
    equivalence_set_id = Column(String, index=True)  # for grouping similar entities
    
    # Relationships
    organization = relationship("Organization", back_populates="entities")
    source_links = relationship("Link", foreign_keys="Link.src_entity_id", back_populates="source_entity")
    target_links = relationship("Link", foreign_keys="Link.dst_entity_id", back_populates="target_entity")
    events = relationship("Event", back_populates="entity")
