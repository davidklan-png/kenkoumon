# Instructions Index

Complete documentation for Kenkoumon setup, configuration, and usage.

## Documentation

| Document | Description | For |
|----------|-------------|-----|
| **[Backend Setup](BACKEND-SETUP.md)** | Install and run the backend API | Developers, DevOps |
| **[iOS Setup](IOS-SETUP.md)** | Build and run the iOS app | iOS Developers |
| **[Configuration](CONFIGURATION.md)** | Configure AI sources, security, deployment | Developers, DevOps |
| **[Usage](USAGE.md)** | End-user guide for the app | Patients, Users |

## Quick Start

### For Users

1. Download Kenkoumon from TestFlight/App Store
2. Create account
3. Record your consultation
4. Share report with your doctor

See [Usage Guide](USAGE.md) for details.

### For Developers

1. Clone repository: `git clone git@github.com:davidklan-png/kenkoumon.git`
2. Set up backend: See [Backend Setup](BACKEND-SETUP.md)
3. Build iOS app: See [iOS Setup](IOS-SETUP.md)
4. Configure AI: See [Configuration Guide](CONFIGURATION.md)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         Kenkoumon                           │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐      ┌────────────┐ │
│  │  iOS App     │      │  Backend     │      │   AI       │ │
│  │              │      │  (FastAPI)   │      │ Services   │ │
│  │  - Record    │◄────►│  - Auth      │◄────►│            │ │
│  │  - Process   │      │  - Sessions  │      │ - On-device│ │
│  │  - Review    │      │  - Reports   │      │ - Ollama   │ │
│  │  - Share     │      │  - Sharing   │      │ - OpenAI   │ │
│  └──────────────┘      └──────────────┘      │ - Anthropic│ │
│                                               │            │ │
│                          ┌──────────────┐    └────────────┘ │
│                          │   Database   │                   │
│                          │   (SQLite)   │                   │
│                          └──────────────┘                   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## AI Source Options

| Source | Privacy | Cost | Setup Difficulty |
|--------|---------|------|------------------|
| **On-Device** | ★★★★★ | Free | Hard |
| **User-Hosted** | ★★★★☆ | Free | Medium |
| **Cloud** | ★★☆☆☆ | Pay-per-use | Easy |

See [Configuration Guide](CONFIGURATION.md) for detailed setup.

---

## Common Tasks

### Set up development environment

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload

# iOS
open ios/Kenkoumon.xcodeproj
# In Xcode: Cmd + R to run
```

### Run tests

```bash
# Backend
cd backend
pytest

# iOS
cd ios
xcodebuild test -scheme Kenkoumon -destination 'platform=iOS Simulator,name=iPhone 15'
```

### Deploy to production

See [Configuration Guide - Deployment Scenarios](CONFIGURATION.md#deployment-scenarios).

---

## File Locations

| Component | Path |
|-----------|------|
| Backend API | `backend/` |
| iOS App | `ios/` |
| Documentation | `docs/` |
| Instructions | `docs/instructions/` |
| Tests | `backend/tests/`, `ios/Tests/` |
| CI/CD | `.github/workflows/` |

---

## Getting Help

- **Documentation:** See individual guides above
- **Issues:** https://github.com/davidklan-png/kenkoumon/issues
- **Email:** support@kenkoumon.example.com

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2025-03-01 | Initial MVP release |
