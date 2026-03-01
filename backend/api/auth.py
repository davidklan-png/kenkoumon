"""
Authentication API endpoints.

Email/password authentication with JWT tokens.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token
)
from core.schemas import LoginRequest, RegisterRequest, TokenResponse
from models import Patient
import uuid

router = APIRouter()
security = HTTPBearer()


def get_current_patient(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Patient:
    """Get the currently authenticated patient from JWT token."""
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    patient_id = payload.get("sub")
    if patient_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Patient not found"
        )

    return patient


@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new patient account.

    - **email**: Patient email address (must be unique)
    - **password**: Password (min 8 characters)
    - **full_name**: Optional full name
    """
    # Check if email already exists
    existing = db.query(Patient).filter(Patient.email == request.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new patient
    patient = Patient(
        id=str(uuid.uuid4()),
        email=request.email,
        hashed_password=get_password_hash(request.password),
        full_name=request.full_name,
    )

    db.add(patient)
    db.commit()

    # Generate access token
    access_token = create_access_token(data={"sub": patient.id})

    return TokenResponse(access_token=access_token)


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login with email and password.

    Returns a JWT access token.
    """
    # Find patient by email
    patient = db.query(Patient).filter(Patient.email == request.email).first()
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(request.password, patient.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate access token
    access_token = create_access_token(data={"sub": patient.id})

    return TokenResponse(access_token=access_token)


@router.get("/me")
async def get_me(current_patient: Patient = Depends(get_current_patient)):
    """Get current patient information."""
    return {
        "id": current_patient.id,
        "email": current_patient.email,
        "full_name": current_patient.full_name,
        "created_at": current_patient.created_at,
    }
