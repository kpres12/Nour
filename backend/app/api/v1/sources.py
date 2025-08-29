from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import json
import os
from app.core.db import get_db
from app.core.models import Dataset, Organization
from app.core.schemas import DatasetCreate, DatasetResponse
from app.deps import get_current_org_id, get_current_org
from app.config import settings

router = APIRouter(prefix="/sources", tags=["data sources"])


@router.post("/", response_model=DatasetResponse)
async def create_dataset(
    dataset: DatasetCreate,
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """Create a new data source/dataset"""
    db_dataset = Dataset(
        **dataset.dict(),
        org_id=org_id
    )
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return db_dataset


@router.get("/", response_model=List[DatasetResponse])
async def list_datasets(
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """List all datasets for the organization"""
    datasets = db.query(Dataset).filter(Dataset.org_id == org_id).all()
    return datasets


@router.post("/upload/{dataset_id}")
async def upload_file(
    dataset_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """Upload a file to a dataset"""
    # Verify dataset belongs to organization
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.org_id == org_id
    ).first()
    
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Create upload directory if it doesn't exist
    upload_dir = os.path.join(settings.UPLOAD_DIR, str(org_id), str(dataset_id))
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "size": len(content),
        "dataset_id": dataset_id
    }


@router.get("/{dataset_id}")
async def get_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """Get dataset details"""
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.org_id == org_id
    ).first()
    
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    return dataset
