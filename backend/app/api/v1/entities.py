from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
from app.core.db import get_db
from app.core.models import Entity, RawRecord, Dataset
from app.core.schemas import EntityCreate, EntityResponse, EntitySearch
from app.deps import get_current_org_id
from app.core.services.resolver_service import EntityResolver

router = APIRouter(prefix="/entities", tags=["entities"])


@router.post("/resolve", response_model=List[EntityResponse])
async def resolve_entities(
    dataset_id: int,
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """Run entity resolution on a dataset"""
    # Verify dataset belongs to organization
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.org_id == org_id
    ).first()
    
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Get raw records
    raw_records = db.query(RawRecord).filter(
        RawRecord.dataset_id == dataset_id,
        RawRecord.status == "processed"
    ).all()
    
    if not raw_records:
        raise HTTPException(status_code=400, detail="No processed records found")
    
    # Run entity resolution
    resolver = EntityResolver()
    entities = resolver.resolve_entities(raw_records, org_id, db)
    
    return entities


@router.get("/", response_model=List[EntityResponse])
async def search_entities(
    query: str = None,
    entity_type: str = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """Search entities"""
    query_obj = db.query(Entity).filter(Entity.org_id == org_id)
    
    if query:
        # Simple text search in canonical data
        query_obj = query_obj.filter(Entity.canonical.contains(query))
    
    if entity_type:
        query_obj = query_obj.filter(Entity.type == entity_type)
    
    entities = query_obj.offset(offset).limit(limit).all()
    return entities


@router.get("/{entity_id}", response_model=EntityResponse)
async def get_entity(
    entity_id: int,
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """Get entity by ID"""
    entity = db.query(Entity).filter(
        Entity.id == entity_id,
        Entity.org_id == org_id
    ).first()
    
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    return entity


@router.post("/", response_model=EntityResponse)
async def create_entity(
    entity: EntityCreate,
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """Create a new entity"""
    db_entity = Entity(
        **entity.dict(),
        org_id=org_id
    )
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    return db_entity
