from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class SignalCreate(BaseModel):
    kind: str
    period_start: datetime
    period_end: datetime
    payload: Dict[str, Any]
    score: float
    threshold: Optional[float] = 0.5


class SignalResponse(BaseModel):
    id: int
    kind: str
    period_start: datetime
    period_end: datetime
    payload: Dict[str, Any]
    score: float
    threshold: float
    
    class Config:
        from_attributes = True
