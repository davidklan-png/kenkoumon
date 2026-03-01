# Configuration Guide

Complete guide for configuring Kenkoumon for different use cases.

## Table of Contents

- [AI Source Selection](#ai-source-selection)
- [Backend Configuration](#backend-configuration)
- [iOS App Configuration](#ios-app-configuration)
- [Security Configuration](#security-configuration)
- [Deployment Scenarios](#deployment-scenarios)

---

## AI Source Selection

Kenkoumon supports three AI sources. Choose based on your privacy, cost, and performance requirements.

### Comparison Table

| Source | Privacy | Cost | Speed | Accuracy | Setup |
|--------|---------|------|-------|----------|-------|
| **On-Device** | Highest | Free | Slowest | Good | Complex |
| **User-Hosted** | High | Free | Medium | Good | Medium |
| **Cloud** | Lowest | Per-use | Fastest | Best | Simple |

### Configuration Matrix

| Scenario | Transcription | Report Generation |
|----------|---------------|-------------------|
| **Maximum Privacy** | On-device | On-device |
| **Home Server** | User-hosted | User-hosted |
| **Best Quality** | Cloud | Cloud |
| **Hybrid** | On-device | Cloud |
| **Offline** | On-device | On-device |

---

## Backend Configuration

### Environment Variables

Create `.env` in the `backend/` directory:

```bash
# =============================================================================
# REQUIRED
# =============================================================================
SECRET_KEY=generate-with-openssl-rand-hex-32

# =============================================================================
# AI SOURCES
# =============================================================================
DEFAULT_TRANSCRIPTION_SOURCE=cloud  # on-device, user-hosted, cloud
DEFAULT_LLM_SOURCE=cloud            # on-device, user-hosted, cloud

# =============================================================================
# CLOUD AI (if using cloud sources)
# =============================================================================
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# =============================================================================
# USER-HOSTED AI (if using user-hosted sources)
# =============================================================================
OLLAMA_URL=http://localhost:11434

# =============================================================================
# DATABASE
# =============================================================================
DATABASE_URL=sqlite:///kenkoumon.db
# For PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost:5432/kenkoumon

# =============================================================================
# CORS (comma-separated)
# =============================================================================
ALLOWED_ORIGINS=http://localhost:3000,kenkoumon://

# =============================================================================
# FILE STORAGE
# =============================================================================
UPLOAD_DIR=uploads
MAX_FILE_SIZE_MB=100
```

### Scenario: Cloud AI (Recommended for MVP)

```bash
DEFAULT_TRANSCRIPTION_SOURCE=cloud
DEFAULT_LLM_SOURCE=cloud
OPENAI_API_KEY=sk-your-key
ANTHROPIC_API_KEY=sk-ant-your-key
```

### Scenario: User-Hosted AI (Ollama)

```bash
DEFAULT_TRANSCRIPTION_SOURCE=user-hosted
DEFAULT_LLM_SOURCE=user-hosted
OLLAMA_URL=http://localhost:11434
```

Required Ollama models:
```bash
ollama pull llama3.1
# For transcription, use LocalAI instead (Ollama doesn't support audio)
```

### Scenario: On-Device AI

Mobile apps handle AI locally. Backend configuration:
```bash
DEFAULT_TRANSCRIPTION_SOURCE=on-device
DEFAULT_LLM_SOURCE=on-device
# No API keys needed
```

---

## iOS App Configuration

### API Configuration

Edit `ios/Shared/Configuration.swift`:

```swift
enum Environment {
    case development
    case staging
    case production

    var baseURL: String {
        switch self {
        case .development:
            return "http://localhost:8000"
        case .staging:
            return "https://staging-api.kenkoumon.example.com"
        case .production:
            return "https://api.kenkoumon.example.com"
        }
    }
}

struct APIConfig {
    static let environment: Environment = .development
    static let baseURL = environment.baseURL
    static let timeout: TimeInterval = 30.0
}
```

### AI Configuration

Edit `ios/Shared/AIConfiguration.swift`:

```swift
enum AISource {
    case onDevice
    case userHosted
    case cloud
}

struct AIConfiguration {
    // Transcription
    static let transcriptionSource: AISource = .cloud
    static let openAIAudioFormat = "m4a"
    static let transcriptionLanguage = "ja"

    // Report Generation
    static let llmSource: AISource = .cloud
    static let cloudLLMProvider: CloudLLMProvider = .claude  // or .gpt

    // API Keys (stored in Keychain)
    static var openAIKey: String? = KeychainService.get(key: "openai_key")
    static var anthropicKey: String? = KeychainService.get(key: "anthropic_key")

    // User-Hosted
    static var ollamaURL: String? = KeychainService.get(key: "ollama_url")
    static var ollamaModel = "llama3.1"

    // On-Device Models
    static let whisperModelName = "whisper-large-v3"
    static let llamaModelName = "llama-3.1-8b-instruct-q4_0"
}
```

### Feature Flags

Edit `ios/Shared/FeatureFlags.swift`:

```swift
struct FeatureFlags {
    // Enable/disable features per environment
    static let enableOnDeviceTranscription = true
    static let enableOnDeviceReportGeneration = false  // Requires powerful device
    static let enableBackgroundProcessing = true
    static let enableAnalytics = false  // Privacy-first
    static let maxRecordingDuration: TimeInterval = 3600  // 1 hour
}
```

---

## Security Configuration

### TLS/HTTPS

**Production (Required):**
```bash
# Use reverse proxy with TLS
# Example: Nginx configuration
server {
    listen 443 ssl http2;
    server_name api.kenkoumon.example.com;

    ssl_certificate /etc/letsencrypt/live/api.kenkoumon.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.kenkoumon.example.com/privkey.pem;
    ssl_protocols TLSv1.3;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Development:**
- HTTP is acceptable for local development
- Use `kenkoumon://` custom scheme for iOS app

### Encryption

**Audio Encryption (AES-256):**

Configure in `backend/core/encryption.py`:

```python
from cryptography.fernet import Fernet

class EncryptionService:
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)

    def encrypt_audio(self, audio_data: bytes) -> bytes:
        return self.cipher.encrypt(audio_data)

    def decrypt_audio(self, encrypted_data: bytes) -> bytes:
        return self.cipher.decrypt(encrypted_data)
```

### Key Management

**Per-Patient Encryption Keys:**

```python
# Each patient has unique encryption key
# Key is derived from password using Argon2
from argon2 import PasswordHasher

hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=4
)
```

---

## Deployment Scenarios

### Scenario 1: Development (Local)

**Backend:**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**iOS:**
```swift
APIConfig.environment = .development
```

### Scenario 2: Self-Hosted (Home Server)

**Hardware:**
- Mac mini, Raspberry Pi 4, or NAS
- 8GB+ RAM recommended
- 64GB+ storage for models

**Backend:**
```bash
# Using Docker Compose
docker-compose up -d
```

**Configuration:**
```bash
DEFAULT_TRANSCRIPTION_SOURCE=user-hosted
DEFAULT_LLM_SOURCE=user-host
OLLAMA_URL=http://localhost:11434
```

**iOS:**
```swift
APIConfig.environment = .production
APIConfig.baseURL = "http://your-home-server.local:8000"
```

### Scenario 3: Cloud Production (AWS)

**Architecture:**
```
                    ┌─────────────┐
                    │   Route53   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   ALB/NLB   │
                    │ (TLS 1.3)   │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
         ┌────▼────┐  ┌───▼────┐  ┌───▼────┐
         │  ECS    │  │  ECS   │  │  ECS   │
         │ Task 1  │  │ Task 2 │  │ Task 3 │
         └─────────┘  └────────┘  └────────┘
              │            │            │
              └────────────┼────────────┘
                           │
                    ┌──────▼──────┐
                    │    RDS      │
                    │ PostgreSQL  │
                    └─────────────┘
```

**Configuration:**
```bash
# Infrastructure as Code (Terraform)
cd infrastructure/terraform
terraform apply

# Environment variables in AWS Secrets Manager
aws secretsmanager create-secret \
  --name kenkoumon/production \
  --secret-string file://.env.production
```

### Scenario 4: Japan Region (APPI Compliance)

**Requirements:**
- All data must remain in Japan
- Use Tokyo region (ap-northeast-1)

**Configuration:**
```bash
# AWS Tokyo
OPENAI_API_BASE=https://tokyo.openai.azure.com  # If available
ANTHROPIC_API_BASE=https://ap-northeast-1.aws.anthropic.com

# Or self-hosted in Japan
OLLAMA_URL=http://tokyo-server.internal:11434
DATABASE_URL=postgresql://user:pass@tokyo-db.example.com/kenkoumon
```

---

## Configuration Checklist

### Backend

- [ ] Generate and set `SECRET_KEY`
- [ ] Configure `DATABASE_URL`
- [ ] Set `ALLOWED_ORIGINS`
- [ ] Configure AI sources
- [ ] Set API keys (if using cloud)
- [ ] Set Ollama URL (if using user-hosted)
- [ ] Configure upload directory
- [ ] Set max file size

### iOS App

- [ ] Set `APIConfig.baseURL`
- [ ] Configure `AIConfiguration`
- [ ] Set `FeatureFlags`
- [ ] Add microphone permission to Info.plist
- [ ] Configure code signing
- [ ] Set app transport security (ATS) exceptions for dev

### Security

- [ ] Enable TLS 1.3 in production
- [ ] Configure AES-256 encryption
- [ ] Set up key rotation
- [ ] Configure rate limiting
- [ ] Enable audit logging
- [ ] Set up intrusion detection

---

## Next Steps

- [ ] Choose AI source based on scenario
- [ ] Configure backend environment variables
- [ ] Configure iOS app settings
- [ ] Test configuration with health check
- [ ] Deploy to target environment
