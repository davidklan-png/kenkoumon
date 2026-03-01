"""
Health check endpoints.
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    ai_sources: dict[str, str]


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check API health and configuration."""
    from core.config import settings

    return HealthResponse(
        status="healthy",
        version="0.1.0",
        ai_sources={
            "transcription": settings.default_transcription_source,
            "llm": settings.default_llm_source,
        }
    )
