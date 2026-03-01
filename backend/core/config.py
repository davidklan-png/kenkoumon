"""
Configuration settings for Kenkoumon backend.
"""

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings."""

    # API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None

    # AI Source Configuration
    default_transcription_source: str = "cloud"  # on-device, user-hosted, cloud
    default_llm_source: str = "cloud"  # on-device, user-hosted, cloud

    # User-hosted AI
    ollama_url: str = "http://localhost:11434"

    # Database
    database_url: str = "sqlite:///kenkoumon.db"

    # JWT
    secret_key: str = "development-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24 hours

    # CORS
    allowed_origins: list[str] = ["http://localhost:3000", "kenkoumon://"]

    # File Storage
    upload_dir: str = "uploads"
    max_file_size_mb: int = 100

    class Config:
        env_file = ".env"

settings = Settings()
