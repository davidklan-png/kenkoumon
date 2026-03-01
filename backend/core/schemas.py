"""
Pydantic schemas for API requests and responses.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# =============================================================================
# Authentication Schemas
# =============================================================================

class LoginRequest(BaseModel):
    """Login request."""
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    """Registration request."""
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: Optional[str] = None


class TokenResponse(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"


# =============================================================================
# Session Schemas
# =============================================================================

class SessionCreate(BaseModel):
    """Create a new session."""
    date: datetime


class SessionUpdate(BaseModel):
    """Update session fields."""
    patient_notes: Optional[str] = None


class SessionResponse(BaseModel):
    """Session response."""
    id: str
    date: datetime
    status: str
    transcript_ja: Optional[str] = None
    report_ja: Optional[str] = None
    patient_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# =============================================================================
# Medication Schemas
# =============================================================================

class MedicationResponse(BaseModel):
    """Medication response."""
    id: str
    name_ja: str
    name_en: Optional[str] = None
    dosage: Optional[str] = None
    status: str
    confidence: Optional[str] = None
    patient_confirmed: bool = False
    date_first_mentioned: Optional[datetime] = None

    class Config:
        from_attributes = True


# =============================================================================
# Condition Schemas
# =============================================================================

class ConditionResponse(BaseModel):
    """Condition response."""
    id: str
    name_ja: str
    name_en: Optional[str] = None
    icd_code: Optional[str] = None
    status: str
    confidence: Optional[str] = None
    patient_confirmed: bool = False

    class Config:
        from_attributes = True


# =============================================================================
# Instruction Schemas
# =============================================================================

class InstructionResponse(BaseModel):
    """Instruction response."""
    id: str
    content_ja: str
    category: str
    due_date: Optional[datetime] = None
    confidence: Optional[str] = None
    patient_confirmed: bool = False

    class Config:
        from_attributes = True


# =============================================================================
# Provider Schemas
# =============================================================================

class ProviderResponse(BaseModel):
    """Provider response."""
    id: str
    name_ja: str
    name_en: Optional[str] = None
    specialty: Optional[str] = None
    clinic_name: Optional[str] = None
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None

    class Config:
        from_attributes = True


# =============================================================================
# Report Schemas
# =============================================================================

class ReportEntity(BaseModel):
    """Extracted entity in report."""
    medications: List[MedicationResponse] = []
    conditions: List[ConditionResponse] = []
    instructions: List[InstructionResponse] = []
    providers: List[ProviderResponse] = []


class ReportResponse(BaseModel):
    """Full report response."""
    id: str
    date: datetime
    status: str
    transcript_ja: Optional[str] = None
    report_ja: Optional[str] = None
    patient_notes: Optional[str] = None
    entities: ReportEntity

    class Config:
        from_attributes = True


# =============================================================================
# Share Link Schemas
# =============================================================================

class ShareLinkCreate(BaseModel):
    """Create share link request."""
    expires_in_days: int = Field(default=30, ge=1, le=365)


class ShareLinkResponse(BaseModel):
    """Share link response."""
    id: str
    token: str
    expires_at: datetime
    url: str

    class Config:
        from_attributes = True


# =============================================================================
# Upload Schemas
# =============================================================================

class AudioUploadResponse(BaseModel):
    """Audio upload response."""
    session_id: str
    status: str
    message: str


# =============================================================================
# Public Report Schemas (for shared links)
# =============================================================================

class PublicReportResponse(BaseModel):
    """Public report view (no auth required)."""
    date: datetime
    transcript_ja: Optional[str] = None
    report_ja: Optional[str] = None
    patient_notes: Optional[str] = None
    entities: ReportEntity
