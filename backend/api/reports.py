"""
Report sharing and public viewing API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
import uuid

from core.database import get_db
from core.config import settings
from core.security import generate_secure_token
from core.schemas import (
    ShareLinkCreate,
    ShareLinkResponse,
    ReportResponse,
    ReportEntity,
    PublicReportResponse,
    MedicationResponse,
    ConditionResponse,
    InstructionResponse,
    ProviderResponse,
)
from api.auth import get_current_patient
from models import (
    Patient,
    Session as DBSession,
    ShareLink,
    Medication,
    Condition,
    Instruction,
    Provider,
)

router = APIRouter()


def _build_report_entities(
    session: DBSession,
    db: Session
) -> ReportEntity:
    """Build entities dict for a session."""
    medications = (
        db.query(Medication)
        .filter(Medication.source_session_id == session.id)
        .all()
    )
    conditions = (
        db.query(Condition)
        .filter(Condition.source_session_id == session.id)
        .all()
    )
    instructions = (
        db.query(Instruction)
        .filter(Instruction.source_session_id == session.id)
        .all()
    )
    providers = (
        db.query(Provider)
        .filter(Provider.source_session_id == session.id)
        .all()
    )

    return ReportEntity(
        medications=[MedicationResponse.model_validate(m) for m in medications],
        conditions=[ConditionResponse.model_validate(c) for c in conditions],
        instructions=[InstructionResponse.model_validate(i) for i in instructions],
        providers=[ProviderResponse.model_validate(p) for p in providers],
    )


@router.get("/{session_id}", response_model=ReportResponse)
async def get_report(
    session_id: str,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    """Get a full report for a session."""
    session = (
        db.query(DBSession)
        .filter(
            DBSession.id == session_id,
            DBSession.patient_id == current_patient.id
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    entities = _build_report_entities(session, db)

    return ReportResponse(
        id=session.id,
        date=session.date,
        status=session.status,
        transcript_ja=session.transcript_ja,
        report_ja=session.report_ja,
        patient_notes=session.patient_notes,
        entities=entities,
    )


@router.post("/{session_id}/share", response_model=ShareLinkResponse)
async def create_share_link(
    session_id: str,
    link_data: ShareLinkCreate,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    """
    Create a secure share link for a report.

    - **expires_in_days**: Number of days until link expires (1-365)
    """
    session = (
        db.query(DBSession)
        .filter(
            DBSession.id == session_id,
            DBSession.patient_id == current_patient.id
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    if session.status != "complete":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot share a report that is not complete"
        )

    # Calculate expiration
    expires_at = datetime.utcnow() + timedelta(days=link_data.expires_in_days)

    # Create share link
    link = ShareLink(
        id=str(uuid.uuid4()),
        session_id=session_id,
        token=generate_secure_token(),
        expires_at=expires_at,
    )

    db.add(link)
    db.commit()

    # Build URL (configure base URL in production)
    base_url = settings.allowed_origins[0] if settings.allowed_origins else "http://localhost:8000"
    url = f"{base_url}/share/{link.token}"

    return ShareLinkResponse(
        id=link.id,
        token=link.token,
        expires_at=link.expires_at,
        url=url,
    )


@router.get("/{session_id}/shares", response_model=list[ShareLinkResponse])
async def list_share_links(
    session_id: str,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    """List all share links for a session."""
    # Verify ownership
    session = (
        db.query(DBSession)
        .filter(
            DBSession.id == session_id,
            DBSession.patient_id == current_patient.id
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    links = (
        db.query(ShareLink)
        .filter(ShareLink.session_id == session_id)
        .order_by(ShareLink.created_at.desc())
        .all()
    )

    # Build URLs
    base_url = settings.allowed_origins[0] if settings.allowed_origins else "http://localhost:8000"

    return [
        ShareLinkResponse(
            id=link.id,
            token=link.token,
            expires_at=link.expires_at,
            url=f"{base_url}/share/{link.token}",
        )
        for link in links
    ]


@router.delete("/shares/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_share_link(
    link_id: str,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    """Revoke a share link."""
    link = db.query(ShareLink).filter(ShareLink.id == link_id).first()

    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Share link not found"
        )

    # Verify ownership through session
    session = (
        db.query(DBSession)
        .filter(
            DBSession.id == link.session_id,
            DBSession.patient_id == current_patient.id
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    link.revoked = True
    db.commit()

    return None


@router.get("/share/{token}", response_model=PublicReportResponse)
async def view_shared_report(
    token: str,
    db: Session = Depends(get_db),
):
    """
    View a shared report (public endpoint, no authentication required).

    - **token**: Share link token
    """
    link = (
        db.query(ShareLink)
        .filter(ShareLink.token == token)
        .first()
    )

    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Share link not found"
        )

    # Check if link is expired or revoked
    if link.revoked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This share link has been revoked"
        )

    if datetime.utcnow() > link.expires_at:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This share link has expired"
        )

    # Get session
    session = (
        db.query(DBSession)
        .filter(DBSession.id == link.session_id)
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    entities = _build_report_entities(session, db)

    return PublicReportResponse(
        date=session.date,
        transcript_ja=session.transcript_ja,
        report_ja=session.report_ja,
        patient_notes=session.patient_notes,
        entities=entities,
    )
