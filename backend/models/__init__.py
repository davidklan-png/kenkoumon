"""
Database models for Kenkoumon.
"""

from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from core.database import Base
import enum
from datetime import datetime


class Status(str, enum.Enum):
    """Session and entity status."""
    UPLOADING = "uploading"
    UPLOADED = "uploaded"
    TRANSCRIBING = "transcribing"
    TRANSCRIBED = "transcribed"
    GENERATING = "generating"
    COMPLETE = "complete"
    FAILED = "failed"
    TRANSCRIPTION_FAILED = "transcription_failed"
    GENERATION_FAILED = "generation_failed"


class MedicationStatus(str, enum.Enum):
    """Medication status."""
    PRESCRIBED = "prescribed"
    CHANGED = "changed"
    DISCONTINUED = "discontinued"
    DISCUSSED = "discussed"


class ConditionStatus(str, enum.Enum):
    """Condition status."""
    ACTIVE = "active"
    MONITORING = "monitoring"
    RESOLVED = "resolved"
    DISCUSSED = "discussed"


class InstructionCategory(str, enum.Enum):
    """Instruction category."""
    LIFESTYLE = "lifestyle"
    MEDICATION = "medication"
    FOLLOW_UP = "follow_up"
    TEST = "test"
    REFERRAL = "referral"


class DocumentCategory(str, enum.Enum):
    """Health document category."""
    HEALTH_CHECKUP = "health_checkup"
    MEDICATION = "medication"
    VACCINATION = "vaccination"
    LAB_RESULTS = "lab_results"
    MEDICAL_CERTIFICATE = "medical_certificate"
    OTHER = "other"


class Patient(Base):
    """Patient account."""
    __tablename__ = "patients"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    encryption_key = Column(String)  # Per-patient encryption key

    # Relationships
    sessions = relationship("Session", back_populates="patient", cascade="all, delete-orphan")
    providers = relationship("Provider", back_populates="patient", cascade="all, delete-orphan")
    medications = relationship("Medication", back_populates="patient", cascade="all, delete-orphan")
    conditions = relationship("Condition", back_populates="patient", cascade="all, delete-orphan")
    instructions = relationship("Instruction", back_populates="patient", cascade="all, delete-orphan")
    health_documents = relationship("HealthDocument", back_populates="patient", cascade="all, delete-orphan")


class Session(Base):
    """Recording session."""
    __tablename__ = "sessions"

    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    audio_reference = Column(String)  # Encrypted path to audio file
    transcript_ja = Column(Text)
    report_ja = Column(Text)
    patient_notes = Column(Text)
    status = Column(String, default=Status.UPLOADING.value)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = relationship("Patient", back_populates="sessions")
    providers = relationship("Provider", back_populates="session", cascade="all, delete-orphan")
    medications = relationship("Medication", back_populates="session", cascade="all, delete-orphan")
    conditions = relationship("Condition", back_populates="session", cascade="all, delete-orphan")
    instructions = relationship("Instruction", back_populates="session", cascade="all, delete-orphan")
    share_links = relationship("ShareLink", back_populates="session", cascade="all, delete-orphan")


class Provider(Base):
    """Medical provider (doctor/clinic)."""
    __tablename__ = "providers"

    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    source_session_id = Column(String, ForeignKey("sessions.id"))
    name_ja = Column(String, nullable=False)
    name_en = Column(String)
    specialty = Column(String)
    clinic_name = Column(String)
    first_seen = Column(DateTime)
    last_seen = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    patient = relationship("Patient", back_populates="providers")
    session = relationship("Session", foreign_keys=[source_session_id])


class Medication(Base):
    """Medication entity."""
    __tablename__ = "medications"

    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    source_session_id = Column(String, ForeignKey("sessions.id"))
    name_ja = Column(String, nullable=False)
    name_en = Column(String)
    dosage = Column(String)
    status = Column(String, default=MedicationStatus.DISCUSSED.value)
    confidence = Column(String)  # high, medium, low
    patient_confirmed = Column(Boolean, default=False)
    date_first_mentioned = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    patient = relationship("Patient", back_populates="medications")
    session = relationship("Session", foreign_keys=[source_session_id])


class Condition(Base):
    """Medical condition entity."""
    __tablename__ = "conditions"

    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    source_session_id = Column(String, ForeignKey("sessions.id"))
    name_ja = Column(String, nullable=False)
    name_en = Column(String)
    icd_code = Column(String)  # ICD-10 code
    status = Column(String, default=ConditionStatus.DISCUSSED.value)
    confidence = Column(String)
    patient_confirmed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    patient = relationship("Patient", back_populates="conditions")
    session = relationship("Session", foreign_keys=[source_session_id])


class Instruction(Base):
    """Instruction entity."""
    __tablename__ = "instructions"

    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    source_session_id = Column(String, ForeignKey("sessions.id"))
    content_ja = Column(Text, nullable=False)
    category = Column(String, default=InstructionCategory.LIFESTYLE.value)
    due_date = Column(DateTime)
    confidence = Column(String)
    patient_confirmed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    patient = relationship("Patient", back_populates="instructions")
    session = relationship("Session", foreign_keys=[source_session_id])


class ShareLink(Base):
    """Secure sharing link."""
    __tablename__ = "share_links"

    id = Column(String, primary_key=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    token = Column(String, unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    revoked = Column(Boolean, default=False)

    # Relationships
    session = relationship("Session", back_populates="share_links")


class HealthDocument(Base):
    """Health document imported from MyNumber Portal or other sources."""
    __tablename__ = "health_documents"

    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    file_name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # MIME type
    file_path = Column(String)  # Encrypted path to stored file
    file_size = Column(Integer)  # Size in bytes
    upload_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    document_date = Column(DateTime)  # Date of the document (e.g., checkup date)
    category = Column(String, default=DocumentCategory.OTHER.value)
    summary = Column(Text)  # Patient notes or AI summary
    tags = Column(String)  # Comma-separated tags
    extracted_data = Column(Text)  # JSON string of extracted health data

    # Relationships
    patient = relationship("Patient", back_populates="health_documents")
