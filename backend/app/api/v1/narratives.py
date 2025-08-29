from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
import json
from app.core.db import get_db
from app.core.models import Narrative, Signal, Rule, Entity
from app.core.schemas import NarrativeCreate, NarrativeResponse
from app.deps import get_current_org_id
from app.core.services.narrative_service import NarrativeService

router = APIRouter(prefix="/narratives", tags=["narratives"])


@router.post("/generate", response_model=NarrativeResponse)
async def generate_narrative(
    narrative: NarrativeCreate,
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """Generate a new narrative"""
    narrative_service = NarrativeService()
    
    # Generate narrative using service
    generated_narrative = narrative_service.generate_narrative(
        title=narrative.title,
        summary=narrative.summary,
        evidence=narrative.evidence or {},
        actions=narrative.actions or [],
        org_id=org_id,
        db=db
    )
    
    return generated_narrative


@router.get("/", response_model=List[NarrativeResponse])
async def list_narratives(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """List narratives for the organization"""
    narratives = db.query(Narrative).filter(
        Narrative.org_id == org_id
    ).order_by(Narrative.created_at.desc()).offset(offset).limit(limit).all()
    
    return narratives


@router.get("/{narrative_id}", response_model=NarrativeResponse)
async def get_narrative(
    narrative_id: int,
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """Get narrative by ID"""
    narrative = db.query(Narrative).filter(
        Narrative.id == narrative_id,
        Narrative.org_id == org_id
    ).first()
    
    if not narrative:
        raise HTTPException(status_code=404, detail="Narrative not found")
    
    return narrative


@router.post("/auto-generate")
async def auto_generate_narratives(
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """Automatically generate narratives based on signals and rules"""
    narrative_service = NarrativeService()
    
    # Get recent signals
    recent_signals = db.query(Signal).filter(
        Signal.org_id == org_id,
        Signal.created_at >= datetime.utcnow() - timedelta(days=7)
    ).all()
    
    # Get active rules
    active_rules = db.query(Rule).filter(
        Rule.org_id == org_id,
        Rule.enabled == True
    ).all()
    
    if not recent_signals or not active_rules:
        raise HTTPException(status_code=400, detail="No signals or rules found for narrative generation")
    
    # Generate narratives
    narratives = narrative_service.auto_generate_narratives(
        signals=recent_signals,
        rules=active_rules,
        org_id=org_id,
        db=db
    )
    
    return {
        "message": f"Generated {len(narratives)} narratives",
        "narratives": narratives
    }


@router.post("/export/{narrative_id}")
async def export_narrative(
    narrative_id: int,
    format: str = "markdown",
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """Export narrative to different formats"""
    narrative = db.query(Narrative).filter(
        Narrative.id == narrative_id,
        Narrative.org_id == org_id
    ).first()
    
    if not narrative:
        raise HTTPException(status_code=404, detail="Narrative not found")
    
    if format == "markdown":
        markdown_content = f"""# {narrative.title}

## Summary
{narrative.summary}

## Evidence
{json.dumps(narrative.evidence, indent=2)}

## Actions
{chr(10).join([f"- {action}" for action in json.loads(narrative.actions)])}

---
Generated on: {narrative.generated_at}
Author: {narrative.author}
"""
        return {"content": markdown_content, "format": "markdown"}
    
    elif format == "json":
        return {
            "content": {
                "title": narrative.title,
                "summary": narrative.summary,
                "evidence": narrative.evidence,
                "actions": json.loads(narrative.actions),
                "generated_at": narrative.generated_at.isoformat(),
                "author": narrative.author
            },
            "format": "json"
        }
    
    else:
        raise HTTPException(status_code=400, detail="Unsupported format. Use 'markdown' or 'json'")
