from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float, Text
from sqlalchemy.orm import relationship
from app.core.models.base import BaseModel


class Signal(BaseModel):
    org_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    kind = Column(String, nullable=False)  # pipeline_velocity_delta, late_invoice_risk, etc.
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    payload = Column(Text, default="{}")  # JSON string of signal data
    score = Column(Float, default=0.0)  # normalized score 0-1
    threshold = Column(Float, default=0.5)  # threshold for triggering
    
    # Relationships
    organization = relationship("Organization", back_populates="signals")
