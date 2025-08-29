from pydantic import BaseModel
from typing import Optional, Dict, Any


class DatasetCreate(BaseModel):
    name: str
    source_type: str
    acl_tag: str
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None


class DatasetResponse(BaseModel):
    id: int
    name: str
    source_type: str
    acl_tag: str
    description: Optional[str] = None
    is_active: bool
    
    class Config:
        from_attributes = True
