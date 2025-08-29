from pydantic import BaseModel
from typing import Optional, Dict, Any


class RuleCreate(BaseModel):
    name: str
    definition: Dict[str, Any]
    priority: Optional[int] = 1
    category: Optional[str] = "general"


class RuleResponse(BaseModel):
    id: int
    name: str
    definition: Dict[str, Any]
    enabled: bool
    priority: int
    category: str
    
    class Config:
        from_attributes = True
