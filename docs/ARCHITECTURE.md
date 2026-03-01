# Kenkoumon — Architecture

## Core Principles
1. **Patient-centric data ownership** — patient controls everything
2. **Entity-centric data model** — medical concepts exist independently of sessions
3. **Bilingual by nature** — every entity carries JP + EN labels
4. **User-controlled AI** — on-device, user-hosted, or optional cloud fallback
5. **Export-first** — data always exportable, patient can leave anytime

## Entity Data Model (Conceptual)

```
Patient
├── Profile (patient_id, name, DOB, blood_type, allergies)
├── Providers[] (name_ja/en, specialty, clinic, first/last_seen, source_sessions)
├── Conditions[] (name_ja/en, icd_code, status, confidence, patient_confirmed)
├── Medications[] (name_ja/en, dosage, frequency, status, prescribing_provider)
├── Instructions[] (content_ja/en, category, status, giving_provider)
├── Sessions[] (date, provider, transcript_ja, summary, doctor_report, patient_notes)
├── Vitals[] (type, value, unit, measured_date, source)
├── LabResults[] (test_name_ja/en, value, unit, reference_range, flag) ← future
├── Documents[] (type, original_file, extracted_data) ← future
└── Biometrics[] (type, value, timestamp, source_device) ← future
```

### Entity Metadata Pattern
Every AI-extracted entity carries:
- **source_session/source_document** — provenance
- **confidence** — high/medium/low
- **patient_confirmed** — boolean

## Processing Pipeline

### User-Controlled AI Architecture

```
Recording → Transcription → Entity Extraction → Report Generation
              ↓                    ↓                    ↓
         ┌─────────────────────────────────────────────────────┐
         │              AI Source Selection                      │
         ├─────────────┬──────────────┬─────────────────────────┤
         │ On-device   │ User-hosted  │ Cloud (optional)        │
         │             │              │                         │
         │ • whisper.cpp              │ • OpenAI Whisper API
         │ • Llama.cpp   │ • Ollama     │ • Claude/GPT-4 API
         │              │ • LocalAI    │ (Japan-region only)    │
         └─────────────┴──────────────┴─────────────────────────┘
                                              │                       │
                                              ▼                       ▼
                                         Entity Store           Doctor Report
                                                                      │
                                                                Secure Link
```

### AI Source Options

| Source | Transcription | Report Generation | Best For |
|--------|---------------|-------------------|----------|
| **On-device** | whisper.cpp (CoreML/MLC) | Llama.cpp / Gemma | Privacy, no ongoing costs, iPhone 14+/flagship Android |
| **User-hosted** | Whisper (Ollama/LocalAI) | Llama/Gemma/Mistral (Ollama/LocalAI) | Users with home server/NAS, older devices |
| **Cloud** (optional) | OpenAI Whisper API | Claude/GPT-4 API | Fallback when local resources insufficient |

**Default:** On-device for flagship devices, user-hosted or cloud as opt-in fallback.

**Experiment Zero:** Manual pipeline supporting all three AI sources for validation.

## Data Residency

### APPI Compliance Approach

| AI Source | APPI Status | Notes |
|-----------|-------------|-------|
| **On-device** | ✅ Compliant | Data never leaves user's device |
| **User-hosted** | ✅ Compliant | User controls where server is located |
| **Cloud (optional)** | Japan-region required | AWS Tokyo, Azure Japan East, or GCP asia-northeast1 only |

**Key Simplification:** On-device and user-hosted AI eliminate the need for Japan-region cloud infrastructure for most users.

**Production:** If cloud fallback is offered, Japan-region deployment is required for that portion only.

## Security (Production — Not Experiment Zero)
- All data encrypted at rest (AES-256) and in transit (TLS 1.3)
- Per-patient encryption keys
- Patient-controlled audio deletion
- Secure links: time-expiring, optional PIN

## AI Service Abstraction Layer

### Interface Design

```typescript
// Transcription Service Interface
interface TranscriptionService {
  transcribe(audioFile: AudioFile, language: string): Promise<Transcript>;
  estimateTime(audioDuration: number): number;
  isAvailable(): Promise<boolean>;
}

// Report Generation Service Interface
interface ReportGenerationService {
  generateReport(transcript: Transcript, prompt: string): Promise<Report>;
  extractEntities(transcript: Transcript): Promise<ExtractedEntities>;
  estimateTime(transcriptLength: number): number;
  isAvailable(): Promise<boolean>;
}
```

### Implementations

#### On-Device (Primary)
- **OnDeviceWhisperService** - whisper.cpp with CoreML (iOS) / MLC (Android)
- **OnDeviceLLMService** - Llama.cpp or Gemma (quantized models)

#### User-Hosted
- **RemoteWhisperService** - HTTP API to Ollama/LocalAI endpoint
- **RemoteLLMService** - HTTP API to Ollama/LocalAI endpoint

#### Cloud (Optional Fallback)
- **CloudWhisperService** - OpenAI Whisper API (Japan-region)
- **CloudLLMService** - Claude (AWS Bedrock Tokyo) or GPT-4 (Azure Japan East)

### Configuration Model

```typescript
type AISource = 'on-device' | 'user-hosted' | 'cloud';

interface AIConfig {
  transcription: {
    source: AISource;
    userHostedUrl?: string;  // For user-hosted
  };
  reportGeneration: {
    source: AISource;
    userHostedUrl?: string;  // For user-hosted
  };
  fallbackEnabled: boolean;  // Auto-fallback to cloud if local fails
}
```

### Device Requirements

| Platform | Minimum | Recommended |
|----------|---------|-------------|
| **iOS** | iPhone 14 (A16) | iPhone 15 Pro (A17 Pro) |
| **Android** | 8GB RAM, Snapdragon 8 Gen 1 | 12GB RAM, Snapdragon 8 Gen 2/3 |
| **User-hosted** | Any device with network | Mac mini, NAS, or home server |

**Note:** Older devices should use user-hosted or optional cloud fallback.

## Future Export Format (Draft)
```
/my-health-data/
├── health-profile.json          ← structured entity model
├── health-summary.md            ← human-readable overview
├── sessions/
│   ├── YYYY-MM-DD-provider.json
│   └── YYYY-MM-DD-provider.md
├── documents/
│   ├── originals/
│   └── extracted .json
└── PRIVACY-WARNING.md
```
