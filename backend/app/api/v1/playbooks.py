from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
from app.core.db import get_db
from app.core.models import Rule, Signal, Entity
from app.core.schemas import RuleCreate, RuleResponse
from app.deps import get_current_org_id
from app.core.services.rule_engine import RuleEngine

router = APIRouter(prefix="/playbooks", tags=["playbooks"])


@router.post("/", response_model=RuleResponse)
async def create_rule(
    rule: RuleCreate,
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """Create a new business rule"""
    db_rule = Rule(
        **rule.dict(),
        org_id=org_id
    )
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule


@router.get("/", response_model=List[RuleResponse])
async def list_rules(
    category: str = None,
    enabled: bool = None,
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """List rules for the organization"""
    query = db.query(Rule).filter(Rule.org_id == org_id)
    
    if category:
        query = query.filter(Rule.category == category)
    
    if enabled is not None:
        query = query.filter(Rule.enabled == enabled)
    
    rules = query.order_by(Rule.priority.desc(), Rule.created_at.desc()).all()
    return rules


@router.get("/{rule_id}", response_model=RuleResponse)
async def get_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """Get rule by ID"""
    rule = db.query(Rule).filter(
        Rule.id == rule_id,
        Rule.org_id == org_id
    ).first()
    
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    return rule


@router.put("/{rule_id}/toggle")
async def toggle_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """Toggle rule enabled/disabled status"""
    rule = db.query(Rule).filter(
        Rule.id == rule_id,
        Rule.org_id == org_id
    ).first()
    
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    rule.enabled = not rule.enabled
    db.commit()
    db.refresh(rule)
    
    return {"message": f"Rule {'enabled' if rule.enabled else 'disabled'}", "rule": rule}


@router.post("/evaluate")
async def evaluate_rules(
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """Evaluate all active rules against current data"""
    rule_engine = RuleEngine()
    
    # Get active rules
    active_rules = db.query(Rule).filter(
        Rule.org_id == org_id,
        Rule.enabled == True
    ).all()
    
    if not active_rules:
        raise HTTPException(status_code=400, detail="No active rules found")
    
    # Get current signals
    signals = db.query(Signal).filter(
        Signal.org_id == org_id
    ).all()
    
    # Evaluate rules
    results = rule_engine.evaluate_rules(active_rules, signals, db)
    
    return {
        "message": f"Evaluated {len(active_rules)} rules",
        "results": results
    }


@router.get("/categories/available")
async def get_available_rule_categories():
    """Get list of available rule categories"""
    return {
        "categories": [
            "sales",
            "finance", 
            "support",
            "operations",
            "marketing",
            "general"
        ]
    }
