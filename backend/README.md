# Kenkoumon Backend

Patient-owned medical consultation recording and AI-powered reports.

## Features

- JWT authentication with email/password
- Recording session management
- AI-powered transcription (Whisper)
- AI-powered report generation (Llama, Claude, GPT-4)
- Entity extraction (medications, conditions, instructions, providers)
- Secure link sharing
- SQLite database with SQLAlchemy ORM

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite (PostgreSQL option for production)
- **Authentication**: JWT tokens
- **AI**: Abstracted layer supporting on-device, user-hosted, and cloud

## Quick Start

### Development

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your API keys (if using cloud AI)

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

```bash
# Build and run
docker-compose up

# Or with Docker directly
docker build -t kenkoumon-backend .
docker run -p 8000:8000 -v $(pwd)/uploads:/app/uploads kenkoumon-backend
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Configuration

Key environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | - | OpenAI API key for Whisper/GPT |
| `ANTHROPIC_API_KEY` | - | Anthropic API key for Claude |
| `OLLAMA_URL` | `http://localhost:11434` | User-hosted Ollama endpoint |
| `DATABASE_URL` | `sqlite:///kenkoumon.db` | Database connection string |
| `SECRET_KEY` | - | JWT signing key (generate with `openssl rand -hex 32`) |

## Project Structure

```
backend/
├── main.py              # FastAPI application
├── core/
│   ├── config.py        # Configuration settings
│   ├── database.py      # Database session management
│   ├── schemas.py       # Pydantic models
│   └── security.py      # Auth utilities
├── models/
│   └── __init__.py      # SQLAlchemy ORM models
├── api/
│   ├── auth.py          # Authentication endpoints
│   ├── sessions.py      # Session management
│   ├── reports.py       # Report sharing
│   └── health.py        # Health check
├── services/
│   ├── ai_service.py    # AI abstraction layer
│   └── entity_extractor.py  # Entity extraction
└── requirements.txt
```

## Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new patient
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Get current patient

### Sessions
- `POST /api/v1/sessions` - Create session
- `GET /api/v1/sessions` - List sessions
- `GET /api/v1/sessions/{id}` - Get session
- `POST /api/v1/sessions/{id}/audio` - Upload audio
- `POST /api/v1/sessions/{id}/transcribe` - Transcribe audio
- `POST /api/v1/sessions/{id}/generate` - Generate report
- `PATCH /api/v1/sessions/{id}` - Update session
- `DELETE /api/v1/sessions/{id}` - Delete session
- `DELETE /api/v1/sessions/{id}/audio` - Delete audio

### Reports
- `GET /api/v1/reports/{id}` - Get report
- `POST /api/v1/reports/{id}/share` - Create share link
- `GET /api/v1/reports/{id}/shares` - List share links
- `DELETE /api/v1/reports/shares/{link_id}` - Revoke link
- `GET /share/{token}` - Public view (no auth)

## Development

```bash
# Run tests
pytest

# Format code
black .
ruff check .

# Type check
mypy .
```
