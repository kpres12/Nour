from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
import json
from app.core.db import get_db
from app.core.models import Signal, RawRecord, Dataset, Entity
from app.core.schemas import SignalCreate, SignalResponse
from app.deps import get_current_org_id
from app.core.services.signal_service import SignalService

router = APIRouter(prefix="/signals", tags=["signals"])


@router.post("/compute", response_model=List[SignalResponse])
async def compute_signals(
    dataset_id: int = None,
    period_days: int = 90,
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """Compute signals for the organization"""
    signal_service = SignalService()
    
    # Set time period
    period_end = datetime.utcnow()
    period_start = period_end - timedelta(days=period_days)
    
    # Compute signals
    signals = signal_service.compute_signals(
        org_id=org_id,
        period_start=period_start,
        period_end=period_end,
        dataset_id=dataset_id,
        db=db
    )
    
    return signals


@router.get("/", response_model=List[SignalResponse])
async def list_signals(
    kind: str = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """List signals for the organization"""
    query = db.query(Signal).filter(Signal.org_id == org_id)
    
    if kind:
        query = query.filter(Signal.kind == kind)
    
    signals = query.order_by(Signal.created_at.desc()).offset(offset).limit(limit).all()
    return signals


@router.get("/{signal_id}", response_model=SignalResponse)
async def get_signal(
    signal_id: int,
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """Get signal by ID"""
    signal = db.query(Signal).filter(
        Signal.id == signal_id,
        Signal.org_id == org_id
    ).first()
    
    if not signal:
        raise HTTPException(status_code=404, detail="Signal not found")
    
    return signal


@router.post("/", response_model=SignalResponse)
async def create_signal(
    signal: SignalCreate,
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """Create a new signal"""
    db_signal = Signal(
        **signal.dict(),
        org_id=org_id
    )
    db.add(db_signal)
    db.commit()
    db.refresh(db_signal)
    return db_signal


@router.get("/types/available")
async def get_available_signal_types():
    """Get list of available signal types"""
    return {
        "signal_types": [
            "pipeline_velocity_delta",
            "late_invoice_risk", 
            "stalled_deal_motif",
            "support_churn_flag",
            "market_headwind",
            "revenue_trend",
            "customer_satisfaction",
            "operational_efficiency"
        ]
    }
