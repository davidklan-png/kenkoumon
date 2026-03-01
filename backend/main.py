"""
Kenkoumon Backend API

FastAPI application with SQLite database, JWT authentication,
and AI service abstraction layer.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import uvicorn

from core.config import settings
from core.database import engine, SessionLocal, get_db
from api import auth, sessions, reports, health

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    # Startup
    from core.database import init_db
    init_db()
    yield
    # Shutdown
    from core.database import close_db
    close_db()

app = FastAPI(
    title="Kenkoumon API",
    description="Patient-owned medical consultation recording and AI-powered reports",
    version="0.1.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(sessions.router, prefix="/api/v1/sessions", tags=["Sessions"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
