"""
Health document API endpoints.

Handles import, storage, and retrieval of health documents
from MyNumber Portal and other sources.
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List
import uuid
import os
import json

from core.database import get_db
from core.config import settings
from core.schemas import (
    HealthDocumentCreateRequest,
    HealthDocumentResponse,
    HealthDocumentUpdateRequest,
)
from api.auth import get_current_patient
from models import Patient, HealthDocument, DocumentCategory
from services.pdf_extractor import PDFHealthDataExtractor

router = APIRouter()


@router.get("", response_model=List[HealthDocumentResponse])
async def list_health_documents(
    skip: int = 0,
    limit: int = 50,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    """List all health documents for the current patient."""
    documents = (
        db.query(HealthDocument)
        .filter(HealthDocument.patient_id == current_patient.id)
        .order_by(HealthDocument.upload_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return documents


@router.post("", response_model=HealthDocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_health_document(
    file: UploadFile = File(...),
    category: Optional[str] = Form(None),
    document_date: Optional[str] = Form(None),
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    """
    Upload a health document (PDF from MyNumber Portal, etc.).

    - **file**: Health document file (PDF, image, etc.)
    - **category**: Document category (health_checkup, medication, etc.)
    - **document_date**: Date of the document (ISO 8601 format)
    """
    # Validate file size
    if file.size and file.size > settings.max_file_size_mb * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum of {settings.max_file_size_mb}MB"
        )

    # Create upload directory
    upload_dir = os.path.join(settings.upload_dir, "health_documents")
    os.makedirs(upload_dir, exist_ok=True)

    # Save file
    doc_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1]
    file_path = os.path.join(upload_dir, f"{doc_id}{file_extension}")

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # Parse document date if provided
    parsed_date = None
    if document_date:
        try:
            parsed_date = datetime.fromisoformat(document_date.replace('Z', '+00:00'))
        except ValueError:
            pass

    # Extract health data from PDF
    extracted_data = None
    if file.content_type == "application/pdf" or file.filename.lower().endswith('.pdf'):
        try:
            extractor = PDFHealthDataExtractor()
            extracted_data = extractor.extract_from_file(file_path)
        except Exception as e:
            # Log but don't fail - extraction is optional
            print(f"PDF extraction failed: {e}")

    # Create database record
    document = HealthDocument(
        id=doc_id,
        patient_id=current_patient.id,
        file_name=file.filename,
        file_type=file.content_type or "application/octet-stream",
        file_path=file_path,
        file_size=os.path.getsize(file_path),
        document_date=parsed_date,
        category=category or DocumentCategory.OTHER.value,
        extracted_data=json.dumps(extracted_data) if extracted_data else None,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


@router.get("/{document_id}", response_model=HealthDocumentResponse)
async def get_health_document(
    document_id: str,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    """Get a specific health document."""
    document = (
        db.query(HealthDocument)
        .filter(
            HealthDocument.id == document_id,
            HealthDocument.patient_id == current_patient.id
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    return document


@router.patch("/{document_id}", response_model=HealthDocumentResponse)
async def update_health_document(
    document_id: str,
    update_data: HealthDocumentUpdateRequest,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    """Update health document metadata."""
    document = (
        db.query(HealthDocument)
        .filter(
            HealthDocument.id == document_id,
            HealthDocument.patient_id == current_patient.id
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    if update_data.category is not None:
        document.category = update_data.category
    if update_data.summary is not None:
        document.summary = update_data.summary
    if update_data.tags is not None:
        document.tags = ",".join(update_data.tags)

    db.commit()
    db.refresh(document)

    return document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_health_document(
    document_id: str,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    """Delete a health document."""
    document = (
        db.query(HealthDocument)
        .filter(
            HealthDocument.id == document_id,
            HealthDocument.patient_id == current_patient.id
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    # Delete file
    if document.file_path and os.path.exists(document.file_path):
        os.remove(document.file_path)

    db.delete(document)
    db.commit()

    return None


@router.get("/{document_id}/download")
async def download_health_document(
    document_id: str,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    """Download the original file."""
    from fastapi.responses import FileResponse

    document = (
        db.query(HealthDocument)
        .filter(
            HealthDocument.id == document_id,
            HealthDocument.patient_id == current_patient.id
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    if not document.file_path or not os.path.exists(document.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    return FileResponse(
        path=document.file_path,
        filename=document.file_name,
        media_type=document.file_type
    )


@router.get("/summary/health")
async def get_health_summary(
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    """Get aggregated health summary from all documents."""
    documents = (
        db.query(HealthDocument)
        .filter(HealthDocument.patient_id == current_patient.id)
        .filter(HealthDocument.extracted_data.isnot(None))
        .order_by(HealthDocument.document_date.desc())
        .all()
    )

    summary = {
        "latest_height": None,
        "latest_weight": None,
        "latest_bmi": None,
        "latest_blood_pressure_systolic": None,
        "latest_blood_pressure_diastolic": None,
        "latest_blood_sugar": None,
        "latest_hba1c": None,
        "document_count": len(documents),
    }

    # Get latest values from most recent documents
    for doc in documents[:10]:  # Check last 10 documents
        if doc.extracted_data:
            try:
                data = json.loads(doc.extracted_data)
                if summary["latest_height"] is None and data.get("height"):
                    summary["latest_height"] = data["height"]
                if summary["latest_weight"] is None and data.get("weight"):
                    summary["latest_weight"] = data["weight"]
                if summary["latest_bmi"] is None and data.get("bmi"):
                    summary["latest_bmi"] = data["bmi"]
                if summary["latest_blood_pressure_systolic"] is None and data.get("blood_pressure_systolic"):
                    summary["latest_blood_pressure_systolic"] = data["blood_pressure_systolic"]
                if summary["latest_blood_pressure_diastolic"] is None and data.get("blood_pressure_diastolic"):
                    summary["latest_blood_pressure_diastolic"] = data["blood_pressure_diastolic"]
                if summary["latest_blood_sugar"] is None and data.get("blood_sugar"):
                    summary["latest_blood_sugar"] = data["blood_sugar"]
                if summary["latest_hba1c"] is None and data.get("hba1c"):
                    summary["latest_hba1c"] = data["hba1c"]
            except json.JSONDecodeError:
                continue

    return summary
