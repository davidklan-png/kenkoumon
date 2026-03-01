# Kenkoumon — MVP Specification

> **This document describes what gets built AFTER Experiment Zero validates the core hypothesis.** Do not begin MVP development until the experiment confirms that AI-generated doctor briefings are accurate and valued by physicians.

---

## MVP Definition

**User story:** As an English-speaking expat in Japan, I record my doctor's appointment on my phone, the app processes the Japanese conversation into a structured report, and I share that report with my doctor via a secure link so they're prepared for my next visit.

**Scope boundary:** One user flow. Record → Process → Review → Share. Nothing else.

---

## Core Features

### F1: Audio Recording

- Record audio within the app
- Support for Japanese-language medical consultations
- Minimum quality: clear enough for accurate transcription in a typical clinic exam room
- On-device storage until upload
- Patient controls start/stop

**Not included:** Background recording, automatic silence detection, noise cancellation (use phone's built-in), multi-device recording.

### F2: Transcription

- Japanese audio → Japanese text
- Medical terminology accuracy is critical (medication names, conditions, procedures)
- API-based: Whisper or equivalent with Japan-region processing
- Processing time: minutes acceptable, not real-time

**Not included:** Real-time transcription, on-device transcription, speaker diarization (nice-to-have, not required).

### F3: Report Generation

- Japanese transcript → Structured Japanese doctor briefing
- Four sections as defined in [REPORT-TEMPLATE.md](REPORT-TEMPLATE.md)
- Entity extraction: medications, conditions, instructions, providers, tests
- Light interpretation layer: communication observations only

**Not included:** English patient summary (Phase 2), cross-visit analysis, clinical interpretation.

### F4: Patient Review

- Patient views the generated report before sharing
- Patient can add notes in Section 4 (患者からのメモ)
- Patient can choose: share immediately OR review and share later

**Not included:** Patient editing of AI-generated sections, version history, collaborative editing.

### F5: Secure Sharing

- Generate a unique, expiring secure link to the report
- Patient shares the link via any channel (email, LINE, print QR code)
- Link opens a read-only Japanese report viewable in any browser
- No login required for the doctor/clinic to view

**Not included:** Analytics on link opens (nice-to-have), clinic portal, EHR integration, access controls beyond link expiration.

### F6: Session History

- Patient sees a chronological list of their recorded sessions
- Each session shows: date, doctor/clinic (if extracted), processing status
- Patient can view past reports

**Not included:** Search, filtering, longitudinal analysis, entity browsing, data export.

---

## Entity Data Model (v1 Scope)

The entity-centric data model is designed for longitudinal expansion but only the following entities are populated in MVP:

```
Patient Account
├── Sessions[]
│   ├── session_id
│   ├── date
│   ├── audio_reference (encrypted)
│   ├── transcript_ja
│   ├── report_ja
│   ├── patient_notes
│   ├── share_links[]
│   └── extracted_entities → references to entities below
├── Providers[]
│   ├── provider_id
│   ├── name_ja
│   ├── name_en (if available)
│   ├── specialty (if mentioned)
│   └── source_session_id
├── Medications[]
│   ├── medication_id
│   ├── name_ja
│   ├── name_en (international name)
│   ├── dosage (if mentioned)
│   ├── status (prescribed | changed | discontinued | discussed)
│   ├── date_first_mentioned
│   └── source_session_id
├── Conditions[]
│   ├── condition_id
│   ├── name_ja
│   ├── name_en
│   ├── status (active | monitoring | resolved | discussed)
│   └── source_session_id
└── Instructions[]
    ├── instruction_id
    ├── content_ja
    ├── category (lifestyle | medication | follow_up | test | referral)
    ├── due_date (if mentioned)
    └── source_session_id
```

**Empty entity slots reserved for future phases:**
- Biometrics (wearables, phone health data)
- LabResults (blood tests, kenkou shindan)
- Documents (imported PDFs, images)
- Imaging (DICOM references)

---

## Technical Stack (POC/MVP)

| Component | Technology | Rationale |
|---|---|---|
| Mobile app | React Native or Flutter | Cross-platform, single codebase |
| Audio recording | Native device APIs | Best quality, simplest approach |
| Audio storage | Encrypted local + cloud upload | Patient controls deletion |
| Transcription | OpenAI Whisper API (or Azure) | Best Japanese accuracy, Japan-region available via Azure |
| Report generation | Claude API (via AWS Bedrock Tokyo) or GPT-4 (via Azure Japan East) | Japan-region data residency |
| Data storage | PostgreSQL or equivalent | Entity-centric model, relational |
| Secure link hosting | Simple web server with token-based access | Minimal infrastructure |
| Authentication | Standard auth (email/password or social) | Patient account management |

**Abstraction requirement:** The AI layer (transcription + generation) must be abstracted behind an interface so providers can be swapped without re-architecture. This is a hard requirement from Decision 3.

---

## Non-Functional Requirements

| Requirement | Target | Notes |
|---|---|---|
| Transcription accuracy | >90% on medical terms | Measured against manual review |
| Report generation time | <5 minutes | Post-upload processing |
| Data residency | Japan region | APPI compliance |
| Audio encryption | AES-256 at rest and in transit | Medical audio is highly sensitive |
| Link expiration | Configurable, default 30 days | Patient controls |
| Uptime | 99% | Acceptable for early product |

---

## Out of Scope (Explicitly Deferred)

| Feature | Deferred To | Reason |
|---|---|---|
| English patient summary | Phase 2 | Core experiment validates Japanese doctor output first |
| Longitudinal analysis | Phase 2 | Requires multiple sessions from same patient |
| Document ingestion | Phase 2 | Different pipeline, not needed for core validation |
| Data export | Phase 2 | Export format decision deferred |
| Wearable integration | Phase 3 | Separate data source, separate pipeline |
| Clinic portal | Phase 3 | Doctor-side product premature |
| Real-time processing | Phase 3+ | Technical complexity, unclear value add |
| Consent flow design | Phase 2 | Manual verbal consent sufficient for early users |
| Billing/payments | Phase 2 | Free for initial validation users |
| On-device transcription | Phase 3+ | Eliminates audio transit, requires model optimization |

---

## Validation Metrics (MVP)

| Metric | Target | Measurement |
|---|---|---|
| Sessions recorded | 50+ across all users | App analytics |
| Report accuracy | No critical errors in >95% of reports | User-reported |
| Share rate | >60% of reports shared with doctor | App analytics |
| User retention (monthly) | >70% record at least 1 session/month | App analytics |
| Doctor feedback | >50% of shared reports get positive reception | User-reported survey |
| Willingness to pay | >60% of active users would pay ¥1,500/month | User survey |
