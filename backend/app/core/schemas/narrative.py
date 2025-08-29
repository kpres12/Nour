from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class NarrativeCreate(BaseModel):
    title: str
    summary: str
    evidence: Optional[Dict[str, Any]] = None
    actions: Optional[List[str]] = None


class NarrativeResponse(BaseModel):
    id: int
    title: str
    summary: str
    evidence: Dict[str, Any]
    actions: List[str]
    generated_at: datetime
    author: str
    status: str
    
    class Config:
        from_attributes = True
