"""
Test configuration and fixtures.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from core.database import Base, get_db
from core.security import get_password_hash

# Test database
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    """Create a test client with a database session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def test_patient(db_session):
    """Create a test patient."""
    from models import Patient
    import uuid

    patient = Patient(
        id=str(uuid.uuid4()),
        email="test@example.com",
        hashed_password=get_password_hash("testpass123"),
        full_name="Test Patient",
    )
    db_session.add(patient)
    db_session.commit()
    db_session.refresh(patient)
    return patient


@pytest.fixture
def auth_headers(client, test_patient):
    """Get authentication headers for a test patient."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "testpass123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_session(db_session, test_patient):
    """Create a test session."""
    from models import Session as DBSession
    from datetime import datetime
    import uuid

    session = DBSession(
        id=str(uuid.uuid4()),
        patient_id=test_patient.id,
        date=datetime.utcnow(),
        status="uploaded",
        transcript_ja="テスト用の文字起こしです。",
        report_ja="# 診察内容の要約\n\nテスト用のレポートです。",
    )
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)
    return session
