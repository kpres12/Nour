from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.models import Organization
from app.config import settings
from typing import Optional

security = HTTPBearer()


def get_current_org_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """Extract organization ID from JWT token"""
    try:
        payload = jwt.decode(credentials.credentials, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        org_id: int = payload.get("org_id")
        if org_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return org_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_org(db: Session = Depends(get_db), org_id: int = Depends(get_current_org_id)) -> Organization:
    """Get current organization from database"""
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    return org


def get_org_db(org_id: int = Depends(get_current_org_id)):
    """Dependency that provides org_id for database queries"""
    return org_id
