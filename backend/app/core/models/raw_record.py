from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.models.base import BaseModel


class RawRecord(BaseModel):
    dataset_id = Column(Integer, ForeignKey("dataset.id"), nullable=False)
    source_pk = Column(String, nullable=False)  # primary key from source system
    payload = Column(Text, nullable=False)  # JSON string of raw data
    status = Column(String, default="pending")  # pending, processed, error
    error_message = Column(Text, nullable=True)
    
    # Relationships
    dataset = relationship("Dataset", back_populates="raw_records")
