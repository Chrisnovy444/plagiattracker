"""
Authentication & Authorization Router
Handles user registration, login, and activation code validation
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import Optional
import secrets
import hashlib

from app.database import get_db
from app.models import User, ActivationCode, CodeStatus, PlanType
from app.config import settings, PLANS

router = APIRouter()


# Pydantic schemas
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ActivateCodeRequest(BaseModel):
    code: str


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: Optional[str]
    plan_type: str
    analyses_remaining: int
    analyses_limit: int
    subscription_expires_at: Optional[datetime]

    class Config:
        from_attributes = True


def hash_password(password: str) -> str:
    """Simple password hashing (use passlib in production)"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return hash_password(plain_password) == hashed_password


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user with trial plan"""

    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user with trial plan
    trial_plan = PLANS["trial"]
    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        full_name=user_data.full_name,
        plan_type=PlanType.TRIAL,
        analyses_remaining=trial_plan["analyses_limit"],
        analyses_limit=trial_plan["analyses_limit"],
        subscription_expires_at=datetime.utcnow() + timedelta(days=trial_plan["validity_days"])
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=UserResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user"""

    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )

    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()

    return user


@router.post("/activate", response_model=UserResponse)
def activate_code(
    request: ActivateCodeRequest,
    email: EmailStr,
    db: Session = Depends(get_db)
):
    """Activate a subscription code"""

    # Get user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get activation code
    code = db.query(ActivationCode).filter(
        ActivationCode.code == request.code.upper()
    ).first()

    if not code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid activation code"
        )

    # Validate code status
    if code.status != CodeStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Code is {code.status.value}"
        )

    # Activate code
    code.status = CodeStatus.USED
    code.user_id = user.id
    code.activated_at = datetime.utcnow()
    code.expires_at = datetime.utcnow() + timedelta(days=code.validity_days)

    # Update user subscription
    user.plan_type = code.plan_type
    user.analyses_remaining = code.analyses_limit
    user.analyses_limit = code.analyses_limit
    user.subscription_expires_at = code.expires_at

    db.commit()
    db.refresh(user)

    return user


@router.get("/me", response_model=UserResponse)
def get_current_user(email: EmailStr, db: Session = Depends(get_db)):
    """Get current user info"""

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.get("/plans")
def get_plans():
    """Get available subscription plans"""
    return {
        "plans": [
            {
                "type": plan_type,
                "name": plan_data["name"],
                "price_fcfa": plan_data["price_fcfa"],
                "analyses_limit": plan_data["analyses_limit"],
                "validity_days": plan_data["validity_days"],
            }
            for plan_type, plan_data in PLANS.items()
        ],
        "contact": {
            "support_email": settings.SUPPORT_EMAIL,
            "partner_phone": settings.PARTNER_PHONE,
        }
    }
