#!/usr/bin/env python3
"""
Ultra-simple local development server for Nour
This creates a basic FastAPI app with demo endpoints
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta, timezone
import jwt
import json

# Create FastAPI app
app = FastAPI(title="Nour - Narrative Intelligence", version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple JWT secret for demo
JWT_SECRET = "demo-secret-key"
JWT_ALGORITHM = "HS256"

@app.get("/")
async def root():
    return {"message": "Nour API is running!", "timestamp": datetime.now().isoformat()}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "nour-backend"}

@app.post("/api/v1/auth/demo-login")
async def demo_login():
    """Demo login that returns a token"""
    # Create a demo token
    payload = {
        "sub": "demo@nour.com",
        "org_id": 1,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/v1/narratives")
async def list_narratives():
    """Demo narratives endpoint"""
    return [
        {
            "id": 1,
            "title": "Sales Pipeline Analysis",
            "summary": "Q4 pipeline shows strong momentum with 3 deals in final stages",
            "evidence": {"highlights": ["3 deals >$100k", "Pipeline velocity +15%", "Win rate 68%"]},
            "actions": ["Schedule executive reviews", "Prepare close plans", "Update forecasts"],
            "generated_at": datetime.now().isoformat()
        },
        {
            "id": 2,
            "title": "Customer Churn Risk Alert",
            "summary": "5 accounts showing early warning signs of churn",
            "evidence": {"highlights": ["Support tickets +40%", "Usage decline", "Contract renewal in 30 days"]},
            "actions": ["Schedule check-ins", "Review support cases", "Prepare retention offers"],
            "generated_at": datetime.now().isoformat()
        }
    ]

@app.get("/api/v1/signals")
async def list_signals():
    """Demo signals endpoint"""
    return [
        {
            "id": 1,
            "kind": "pipeline_velocity_delta",
            "score": 0.85,
            "value": "+15%",
            "period_start": "2024-01-01",
            "period_end": "2024-01-31"
        },
        {
            "id": 2,
            "kind": "late_invoice_risk",
            "score": 0.72,
            "value": "$45k",
            "period_start": "2024-01-01",
            "period_end": "2024-01-31"
        }
    ]

@app.get("/api/v1/entities")
async def list_entities():
    """Demo entities endpoint"""
    return [
        {
            "id": 1,
            "type": "Account",
            "name": "Acme Corp",
            "confidence": 0.95,
            "properties": {"industry": "Technology", "size": "Enterprise"}
        },
        {
            "id": 2,
            "type": "Person",
            "name": "John Smith",
            "confidence": 0.88,
            "properties": {"title": "VP Sales", "email": "john@acme.com"}
        }
    ]

@app.get("/api/v1/playbooks")
async def list_playbooks():
    """Demo playbooks/rules endpoint"""
    return [
        {
            "id": 1,
            "name": "Pipeline Velocity Alert",
            "description": "Alert when pipeline velocity drops below threshold",
            "enabled": True,
            "definition": {
                "when": "pipeline_velocity < 0.5",
                "then": "Send alert to sales team"
            }
        },
        {
            "id": 2,
            "name": "Churn Risk Detection",
            "description": "Identify accounts at risk of churn",
            "enabled": True,
            "definition": {
                "when": "support_tickets > 5 AND usage_decline > 0.3",
                "then": "Schedule retention call"
            }
        }
    ]

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Nour simple local server...")
    print("🌐 Server will be available at http://localhost:8000")
    print("📚 API documentation at http://localhost:8000/docs")
    print("🔑 Use POST /api/v1/auth/demo-login to get a token")
    print("")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
