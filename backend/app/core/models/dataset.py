from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from app.core.models.base import BaseModel


class Dataset(BaseModel):
    name = Column(String, nullable=False)
    org_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    source_type = Column(String, nullable=False)  # csv, api, webhook, etc.
    acl_tag = Column(String, nullable=False)  # for row-level security
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    config = Column(Text, default="{}")  # JSON string for source-specific config
    
    # Relationships
    organization = relationship("Organization", back_populates="datasets")
    raw_records = relationship("RawRecord", back_populates="dataset")
