from pydantic import BaseModel
from typing import Optional, Dict, Any, List


class EntityCreate(BaseModel):
    type: str
    canonical: Dict[str, Any]
    external_id: Optional[str] = None
    confidence: Optional[float] = 1.0


class EntityResponse(BaseModel):
    id: int
    type: str
    canonical: Dict[str, Any]
    confidence: float
    external_id: Optional[str] = None
    
    class Config:
        from_attributes = True


class EntitySearch(BaseModel):
    query: Optional[str] = None
    type: Optional[str] = None
    limit: int = 50
    offset: int = 0
