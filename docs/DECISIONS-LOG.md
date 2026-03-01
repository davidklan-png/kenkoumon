# Kenkoumon — Architectural Decisions Log

All architectural decisions made during initial design, with rationale and impact.

---

## Phase 1: Foundational Positioning

### Decision 1: Medical Device or Wellness Tool?
**Decision:** Wellness tool. Patient-controlled, assists doctor communication.
**Impact:** Avoids PMDA SaMD classification. Reduces liability. Limits output framing to observations, not clinical assessments.

### Decision 2: Data Ownership
**Decision:** Patient has full control. Doctor interprets at discretion.
**Impact:** All architecture is patient-centric. No clinic/doctor accounts. More complex consent flows but enables network effect.

### Decision 3: Build vs. Buy AI Stack
**Decision:** POC with available tech (Whisper, Claude/GPT-4). Adjust for privacy/residency later.
**Impact:** Zero infrastructure for Experiment Zero. Must abstract AI layer for future swaps. Data residency constraint for production.

### Decision 4: Processing Timing
**Decision:** Patient chooses when to process and release. Options: immediate send or review-then-send.
**Impact:** No real-time requirements. Two processing paths needed. Simpler architecture.

### Decision 5: Market Approach
**Decision:** Eventually two-sided. Deferred for now.
**Impact:** V1 is patient-only, B2C. No clinic portal or enterprise sales.

---

## Phase 2: Product Architecture

### Decision 6: Doctor Delivery
**Decision:** Secure link. Patient generates URL, shares however they choose.
**Impact:** Zero clinic-side integration. Basic open analytics. Can layer portal later.

### Decision 7: Profile Continuity
**Decision:** Longitudinal profile. Complete patient health data silo including biometrics, phone health, everything.
**Impact:** Expands scope from session tool to health data platform. Entity-centric architecture required. Most consequential long-term decision.

### Decision 8: Recording Technology
**Decision:** Patient-controlled. Bootstrap for POC.
**Impact:** Any recording method works. Privacy architecture deferred to post-validation.

### Decision 9: Consent Flow
**Decision:** Deferred.
**Impact:** Verbal consent for Experiment Zero. Must design before public launch.

### Decision 10: Report Content
**Decision:** Basics for doctor's notes, next-visit prep, comprehensive patient understanding.
**Impact:** Report in Japanese medical register. See DOCTOR-REPORT-SPEC.md.

### Decision 11: Localization
**Decision:** Japanese first. Go-to app for expats/tourists in Japan.
**Impact:** Japanese transcription is critical path. Bilingual entity mapping from day one. Target: 3M+ foreign residents.

---

## Phase 3: Data Architecture

### Decision 12: Data Model
**Decision:** Entity-centric.
**Impact:** 2-3 weeks extra modeling. Every entity needs canonical ID, source, timestamp, bilingual labels, confidence. Supports future data sources.

### Decision 13: AI Role
**Decision:** Extraction + one interpretation layer (communication preferences, emotional tone).
**Impact:** Reports include "patient asked about side effects twice" but not "patient has health anxiety." Interpretation expansion is deliberate future decision.

### Decision 14: Language Architecture
**Decision:** Transcribe in source language (Japanese), maintain bilingual entity mappings.
**Impact:** Entity model needs localization layer. Medical terminology databases (MedDRA) bootstrap bilingual mapping.

### Decision 15: "Share With My AI"
**Decision:** Patient dumps data in folder, uses any AI. Must be educated on PHI risks per AI provider.
**Impact:** Company is health data infrastructure, not health AI. Revenue from pipeline (recording → structuring → maintaining), not AI insights. Export format becomes core feature.

---

## Phase 4: Implementation

### Decision 16: Export Format
**Decision:** Deferred until MVP complete.

### Decision 17: Document Ingestion
**Decision:** Deferred. User dumps data in many formats, expects processing.

### Decision 18: PHI Risk Communication
**Decision:** Tiered export with user education on privacy considerations.
**Impact:** Full vs. de-identified export options. Privacy education in product UX.

### Decision 19: MVP Scope Lock
**Decision:** First visit only. Record → process → Japanese report for doctor. Decide next steps based on result.
**Impact:** Experiment Zero IS the MVP. No app, no infra. Manual pipeline. ~2 hours + 2 appointments.

### Decision 20: Report Content Structure
**Decision:** Four sections: Visit Summary, Key Medical Info (structured), Next Visit Prep (observations), Patient Notes (blank).
**Impact:** See DOCTOR-REPORT-SPEC.md and PROCESSING-PROMPT.md.
