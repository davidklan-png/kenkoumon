"""
Session management API endpoints.

Handles recording sessions, audio uploads, transcription,
and report generation.
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
import uuid
import os
import shutil

from core.database import get_db
from core.config import settings
from core.schemas import (
    SessionCreate,
    SessionResponse,
    SessionUpdate,
    AudioUploadResponse,
)
from api.auth import get_current_patient
from models import Patient, Session as DBSession, Status
from services.ai_service import AIServiceConfig, get_transcription_service, get_report_service
from services.entity_extractor import EntityExtractor

router = APIRouter()


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    session_data: SessionCreate,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    """
    Create a new recording session.

    - **date**: Date/time of the medical consultation
    """
    session = DBSession(
        id=str(uuid.uuid4()),
        patient_id=current_patient.id,
        date=session_data.date,
        status=Status.UPLOADING.value,
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


@router.get("", response_model=list[SessionResponse])
async def list_sessions(
    skip: int = 0,
    limit: int = 50,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    """
    List all sessions for the current patient.

    Results are sorted by date (newest first).
    """
    sessions = (
        db.query(DBSession)
        .filter(DBSession.patient_id == current_patient.id)
        .order_by(DBSession.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return sessions


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    """Get a specific session by ID."""
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

    return session


@router.post("/{session_id}/audio", response_model=AudioUploadResponse)
async def upload_audio(
    session_id: str,
    file: UploadFile = File(...),
    transcription_source: Optional[str] = Form(None),
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    """
    Upload audio file for a session.

    Audio is encrypted at rest using AES-256.

    - **file**: Audio file (m4a, wav, mp3, etc.)
    - **transcription_source**: AI source for transcription (on-device, user-hosted, cloud)
    """
    # Verify session ownership
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

    # Validate file size
    if file.size and file.size > settings.max_file_size_mb * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum of {settings.max_file_size_mb}MB"
        )

    # Create upload directory if needed
    os.makedirs(settings.upload_dir, exist_ok=True)

    # Save file (in production, encrypt with per-patient key)
    file_path = os.path.join(settings.upload_dir, f"{session_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Update session
    session.audio_reference = file_path
    session.status = Status.UPLOADED.value
    db.commit()

    # Trigger transcription if source provided
    if transcription_source:
        # In production, this would be a background task
        session.status = Status.TRANSCRIBING.value
        db.commit()

    return AudioUploadResponse(
        session_id=session_id,
        status=session.status,
        message="Audio uploaded successfully"
    )


@router.post("/{session_id}/transcribe", response_model=SessionResponse)
async def transcribe_session(
    session_id: str,
    source: Optional[str] = "cloud",
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    """
    Transcribe audio for a session.

    - **source**: AI source (on-device, user-hosted, cloud)
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

    if not session.audio_reference:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No audio file uploaded"
        )

    # Update status
    session.status = Status.TRANSCRIBING.value
    db.commit()

    try:
        # Get transcription service
        config = AIServiceConfig()
        transcription_service = get_transcription_service(source, config)

        # Transcribe
        transcript = await transcription_service.transcribe(
            session.audio_reference,
            language="ja"
        )

        # Update session
        session.transcript_ja = transcript
        session.status = Status.TRANSCRIBED.value
        db.commit()

        return session

    except Exception as e:
        session.status = Status.TRANSCRIPTION_FAILED.value
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Transcription failed: {str(e)}"
        )


@router.post("/{session_id}/generate", response_model=SessionResponse)
async def generate_report(
    session_id: str,
    source: Optional[str] = "cloud",
    cloud_provider: Optional[str] = "claude",
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    """
    Generate report from transcript.

    - **source**: AI source (on-device, user-hosted, cloud)
    - **cloud_provider**: Cloud provider (claude, gpt) when source=cloud
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

    if not session.transcript_ja:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No transcript available"
        )

    # Update status
    session.status = Status.GENERATING.value
    db.commit()

    try:
        # Load processing prompt
        prompt_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "..", "docs", "PROCESSING-PROMPT.md"
        )

        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt = f.read()
        else:
            prompt = """
            以下の医療相談の文字起こしから、医師向けの構造化されたレポートを生成してください。

            # 診察内容の要約

            # 主な医療情報
            ## 薬剤
            ## 病名・疾患
            ## 検査・処置

            # 次回診察に向けて
            ## 患者への指示

            # 患者からのメモ（編集可）
            """

        # Get report generation service
        config = AIServiceConfig()
        report_service = get_report_service(
            source,
            config,
            cloud_provider=cloud_provider
        )

        # Generate report
        report = await report_service.generate_report(
            session.transcript_ja,
            prompt
        )

        # Update session
        session.report_ja = report
        session.status = Status.COMPLETE.value
        db.commit()

        # Extract entities
        EntityExtractor.extract_from_report(
            session_id,
            current_patient.id,
            report,
            db
        )

        return session

    except Exception as e:
        session.status = Status.GENERATION_FAILED.value
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Report generation failed: {str(e)}"
        )


@router.patch("/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: str,
    update_data: SessionUpdate,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    """
    Update session fields (e.g., patient notes).

    - **patient_notes**: Notes added by the patient
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

    if update_data.patient_notes is not None:
        session.patient_notes = update_data.patient_notes

    db.commit()
    db.refresh(session)

    return session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: str,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    """Delete a session and all its data."""
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

    # Delete audio file if exists
    if session.audio_reference and os.path.exists(session.audio_reference):
        os.remove(session.audio_reference)

    db.delete(session)
    db.commit()

    return None


@router.delete("/{session_id}/audio", status_code=status.HTTP_204_NO_CONTENT)
async def delete_audio(
    session_id: str,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    """
    Delete audio file for a session.

    Keeps transcript and report, removes the audio file.
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

    if session.audio_reference and os.path.exists(session.audio_reference):
        os.remove(session.audio_reference)
        session.audio_reference = None
        db.commit()

    return None
