from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt
from passlib.context import CryptContext
from app.core.db import get_db
from app.core.models import Organization
from app.core.schemas import Token, UserLogin
from app.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = timedelta(minutes=expires_delta)
    else:
        expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token"""
    # For MVP, we'll use a simple demo organization
    # In production, this would validate against user accounts
    
    # Create demo org if it doesn't exist
    org = db.query(Organization).filter(Organization.name == "Demo Organization").first()
    if not org:
        org = Organization(
            name="Demo Organization",
            domain="demo.nour.com"
        )
        db.add(org)
        db.commit()
        db.refresh(org)
    
    # For demo purposes, accept any email/password
    # In production, validate against user table
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_credentials.email, "org_id": org.id},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/demo-login", response_model=Token)
async def demo_login(db: Session = Depends(get_db)):
    """Demo login that creates a demo organization and returns token"""
    # Create demo org if it doesn't exist
    org = db.query(Organization).filter(Organization.name == "Demo Organization").first()
    if not org:
        org = Organization(
            name="Demo Organization",
            domain="demo.nour.com"
        )
        db.add(org)
        db.commit()
        db.refresh(org)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": "demo@nour.com", "org_id": org.id},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
