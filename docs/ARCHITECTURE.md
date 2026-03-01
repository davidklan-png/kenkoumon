# Kenkoumon — Architecture

## Core Principles
1. **Patient-centric data ownership** — patient controls everything
2. **Entity-centric data model** — medical concepts exist independently of sessions
3. **Bilingual by nature** — every entity carries JP + EN labels
4. **AI-layer abstraction** — swappable AI providers
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

```
Recording → Transcription (Whisper/JP) → Extraction (LLM) → Report Generation (LLM)
                                              │                       │
                                              ▼                       ▼
                                         Entity Store           Doctor Report
                                                                      │
                                                                Secure Link
```

**Experiment Zero:** Manual pipeline, no infrastructure.

## Data Residency (Production)
- APPI requires medical data stays in Japan
- Compliant: AWS Tokyo, Azure Japan East, GCP asia-northeast1
- Compliant AI APIs: Azure OpenAI (Japan East), AWS Bedrock (Tokyo)
- POC: Direct API calls acceptable; production requires Japan-region

## Security (Production — Not Experiment Zero)
- All data encrypted at rest (AES-256) and in transit (TLS 1.3)
- Per-patient encryption keys
- Patient-controlled audio deletion
- Secure links: time-expiring, optional PIN

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
