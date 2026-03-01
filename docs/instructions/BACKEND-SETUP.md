# Backend Setup Guide

Complete guide for setting up and running the Kenkoumon backend API.

## Prerequisites

- Python 3.11 or later
- pip (Python package manager)
- (Optional) Docker and Docker Compose
- (Optional) API keys for cloud AI services

---

## Installation

### 1. Clone Repository

```bash
git clone git@github.com:davidklan-png/kenkoumon.git
cd kenkoumon/backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```bash
# Required for production
SECRET_KEY=your-secret-key-here-generate-with-openssl-rand-hex-32

# Optional - for cloud AI fallback
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Optional - for user-hosted AI
OLLAMA_URL=http://localhost:11434

# AI Source Selection
DEFAULT_TRANSCRIPTION_SOURCE=cloud  # or: user-hosted
DEFAULT_LLM_SOURCE=cloud            # or: user-hosted

# Database (default is SQLite)
DATABASE_URL=sqlite:///kenkoumon.db

# CORS
ALLOWED_ORIGINS=http://localhost:3000,kenkoumon://
```

### 5. Generate Secret Key (Production)

```bash
openssl rand -hex 32
```

Use the output as your `SECRET_KEY`.

---

## Running

### Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

- API Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Mode

```bash
docker-compose up
```

---

## AI Service Configuration

### Cloud AI (Optional)

**OpenAI Whisper + GPT-4:**
- Sign up at https://platform.openai.com
- Create API key
- Set `OPENAI_API_KEY` in `.env`

**Anthropic Claude:**
- Sign up at https://console.anthropic.com
- Create API key
- Set `ANTHROPIC_API_KEY` in `.env`

### User-Hosted AI

**Ollama:**
1. Install Ollama: https://ollama.ai
2. Pull models:
   ```bash
   ollama pull llama3.1
   ```
3. Set `OLLAMA_URL=http://localhost:11434` in `.env`
4. Set `DEFAULT_LLM_SOURCE=user-hosted` in `.env`

**LocalAI (for Whisper + LLM):**
1. Install LocalAI: https://localai.io
2. Configure with Whisper and LLM models
3. Set `OLLAMA_URL=http://localhost:11434` to your LocalAI endpoint

### On-Device AI

For mobile apps, AI runs directly on the device. The backend receives:
- Transcripts (not audio) from mobile Whisper
- Reports (not transcripts) from mobile LLM

---

## Database Setup

### SQLite (Default)

SQLite is used by default. The database file (`kenkoumon.db`) is created automatically on first run.

### PostgreSQL (Production)

1. Install PostgreSQL
2. Create database:
   ```sql
   CREATE DATABASE kenkoumon;
   ```
3. Update `.env`:
   ```bash
   DATABASE_URL=postgresql://user:password@localhost/kenkoumon
   ```

---

## Verification

### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "ai_sources": {
    "transcription": "cloud",
    "llm": "cloud"
  }
}
```

### Test Registration

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "full_name": "Test User"
  }'
```

---

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

---

## Troubleshooting

### Import Errors

```bash
# Ensure you're in the backend directory
cd backend

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Database Locked (SQLite)

SQLite locks during writes. If you see "database is locked":
```bash
# Stop all running instances
pkill -f uvicorn

# Remove lock file
rm kenkoumon.db-wal kenkoumon.db-shm
```

### API Key Errors

Ensure API keys are set in `.env`:
```bash
echo $OPENAI_API_KEY  # Should not be empty
```

### Ollama Connection Failed

```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if not running
ollama serve
```

---

## Production Deployment

### Environment Variables

Required for production:
- `SECRET_KEY` - Generate with `openssl rand -hex 32`
- `DATABASE_URL` - PostgreSQL connection string
- `ALLOWED_ORIGINS` - Comma-separated list of allowed origins

### Security Checklist

- [ ] Set strong `SECRET_KEY`
- [ ] Use PostgreSQL (not SQLite)
- [ ] Enable HTTPS/TLS 1.3
- [ ] Set restrictive `ALLOWED_ORIGINS`
- [ ] Use environment variables for API keys
- [ ] Enable database encryption at rest
- [ ] Configure firewall rules
- [ ] Set up log aggregation
- [ ] Enable rate limiting

### Docker Production

```bash
docker build -t kenkoumon-backend .
docker run -d \
  --name kenkoumon-api \
  -p 8000:8000 \
  -v /path/to/uploads:/app/uploads \
  -v /path/to/database:/app/data \
  --env-file .env.production \
  kenkoumon-backend
```

---

## Next Steps

- [ ] Configure AI service (cloud, user-hosted, or on-device)
- [ ] Set up database (SQLite for dev, PostgreSQL for prod)
- [ ] Run tests to verify setup
- [ ] Deploy to production environment
- [ ] Configure mobile app to connect to API
