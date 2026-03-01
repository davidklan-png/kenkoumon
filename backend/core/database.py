"""
Database configuration and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

# Create SQLite engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False)

# Base class for models
Base = declarative_base()

# Database initialization and cleanup
_db_initialized = False

def init_db():
    """Initialize the database with all tables."""
    global _db_initialized
    if not _db_initialized:
        from models import Patient, Session, Provider, Medication, Condition, Instruction, ShareLink
        Base.metadata.create_all(bind=engine)
        _db_initialized = True

def close_db():
    """Close the database connection."""
    global _db_initialized
    if _db_initialized:
        engine.dispose()
        _db_initialized = False

def get_db():
    """Dependency injection for database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
