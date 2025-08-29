from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import json
import os
from datetime import datetime
from app.core.db import get_db
from app.core.models import Dataset, RawRecord, Organization
from app.deps import get_current_org_id
from app.config import settings

router = APIRouter(prefix="/ingest", tags=["data ingestion"])


async def process_csv_file(dataset_id: int, org_id: int, db: Session):
    """Background task to process CSV file"""
    try:
        # Get dataset
        dataset = db.query(Dataset).filter(
            Dataset.id == dataset_id,
            Dataset.org_id == org_id
        ).first()
        
        if not dataset:
            return
        
        # Find uploaded files
        upload_dir = os.path.join(settings.UPLOAD_DIR, str(org_id), str(dataset_id))
        if not os.path.exists(upload_dir):
            return
        
        csv_files = [f for f in os.listdir(upload_dir) if f.endswith('.csv')]
        
        for filename in csv_files:
            file_path = os.path.join(upload_dir, filename)
            
            try:
                # Read CSV
                df = pd.read_csv(file_path)
                
                # Convert to records
                for index, row in df.iterrows():
                    raw_record = RawRecord(
                        dataset_id=dataset_id,
                        source_pk=str(index),
                        payload=json.dumps(row.to_dict()),
                        status="processed"
                    )
                    db.add(raw_record)
                
                db.commit()
                
            except Exception as e:
                # Log error and continue with next file
                print(f"Error processing {filename}: {str(e)}")
                continue
                
    except Exception as e:
        print(f"Error in background task: {str(e)}")


@router.post("/run/{dataset_id}")
async def run_ingestion(
    dataset_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """Start ingestion process for a dataset"""
    # Verify dataset belongs to organization
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.org_id == org_id
    ).first()
    
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Start background processing
    background_tasks.add_task(process_csv_file, dataset_id, org_id, db)
    
    return {
        "message": "Ingestion started",
        "dataset_id": dataset_id,
        "status": "processing"
    }


@router.get("/status/{dataset_id}")
async def get_ingestion_status(
    dataset_id: int,
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """Get ingestion status for a dataset"""
    # Verify dataset belongs to organization
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.org_id == org_id
    ).first()
    
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Count records by status
    total_records = db.query(RawRecord).filter(
        RawRecord.dataset_id == dataset_id
    ).count()
    
    processed_records = db.query(RawRecord).filter(
        RawRecord.dataset_id == dataset_id,
        RawRecord.status == "processed"
    ).count()
    
    error_records = db.query(RawRecord).filter(
        RawRecord.dataset_id == dataset_id,
        RawRecord.status == "error"
    ).count()
    
    return {
        "dataset_id": dataset_id,
        "total_records": total_records,
        "processed_records": processed_records,
        "error_records": error_records,
        "status": "complete" if total_records > 0 and processed_records == total_records else "processing"
    }
