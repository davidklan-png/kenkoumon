# Kenkoumon — Product Vision

## The One-Liner

Kenkoumon is the patient-owned health data platform that turns every medical interaction into structured, bilingual, portable intelligence — controlled entirely by the patient.

---

## Phase 0: Experiment Zero (Now → 2 weeks)

**Goal:** Validate that AI-generated doctor briefings from recorded consultations are accurate and useful.

**What exists:**
- A prompt template
- A manual workflow (record → transcribe → generate → share)
- One user (you)

**Success means:** A Japanese doctor reads the AI-generated briefing and says "I want this before every visit."

---

## Phase 1: Personal Tool (2 weeks → 90 days)

**Goal:** Build a functional app that does for you reliably what the experiment did manually, and validate with 5-10 other expats.

**What gets built:**
- Mobile recording within the app (iOS priority)
- Automated transcription pipeline (Whisper, Japan-region)
- Report generation via LLM API
- Secure link generation for sharing with doctors
- Basic patient account with session history
- Entity extraction into structured data model (medications, conditions, providers, instructions)

**What does NOT get built:**
- Longitudinal insights (cross-visit analysis)
- Document ingestion (kenkou shindan, blood tests)
- Data export
- Clinic-side anything
- Billing/payments

**Success means:** 5+ expats use it for real appointments and confirm they'd pay.

---

## Phase 2: Paying Product (90 days → 12 months)

**Goal:** Launch as a subscription product for English-speaking expats in Japan.

**What gets built:**
- Subscription billing (¥1,500/month)
- Longitudinal profile — cross-visit insights ("compared to your last visit...")
- English patient summary (bilingual output)
- Document ingestion v1 — photo/scan import for kenkou shindan and blood tests
- Entity model fully populated from visits + imported documents
- Data export v1 — structured JSON + markdown + source documents
- PHI risk education and tiered export (full vs. de-identified)
- Patient notes and annotations on reports

**What does NOT get built:**
- Clinic portal or doctor-side product
- Apple HealthKit / wearable integration
- Real-time processing
- Conversational AI query interface
- Multi-language beyond Japanese input / English+Japanese output

**Target:** 100 paying subscribers. ¥150K/month MRR.

**Success means:** Retention >80% at 3 months. Doctors at multiple clinics recognize and value the reports.

---

## Phase 3: Health Data Platform (12 months → 24 months)

**Goal:** Expand from visit intelligence to comprehensive patient-owned health data.

**What gets built:**
- Apple HealthKit / Google Fit integration (biometrics, activity, sleep)
- Wearable data import
- Pharmacy data import (お薬手帳 integration where available)
- Expanded document ingestion (prescriptions, imaging referrals, specialist letters)
- Conversational AI preparation — data model optimized for LLM querying
- Standardized export format (published, documented schema)
- Additional language support (Chinese, Korean input)
- Basic clinic-facing features (receive reports from multiple patients via portal)

**Target:** 1,000 subscribers. Expansion into Korean expats, Chinese expats, medical tourism use cases.

**Success means:** Patients use Kenkoumon as their primary health data repository, not just a visit recording tool.

---

## Phase 4: The Platform (24 months → 5 years)

**Goal:** Patient-owned health data standard. Any medical interaction, any data source, any country, any AI.

**Vision:**
- Every medical interaction flows into the patient's vault: visits, telehealth, pharmacy, lab, imaging
- The patient carries their complete health profile between providers, across borders
- Any AI (cloud or local) can query the patient's data with their explicit consent
- The export format becomes a recognized standard for patient-portable health data
- Expansion beyond expats: any patient who wants to own their health data
- Geographic expansion: Korea, Singapore, US expat clinics, medical tourism hubs

**Potential revenue streams:**
- Patient subscription (core)
- Clinic subscription (receive patient reports, prepare for visits)
- Insurance partnerships (improved adherence, reduced no-shows)
- Platform API (third-party health apps can read/write to the patient's vault with consent)
- De-identified aggregate data insights (only with explicit patient opt-in)

**The moat at 5 years:**
- Patient-owned longitudinal data that grows more valuable over time (switching cost)
- Published export format with ecosystem adoption (network effect)
- Bilingual medical entity database refined across millions of consultations (data moat)
- Trust reputation with privacy-conscious users (brand moat)

---

## What This Is NOT

- **Not a medical device.** Does not provide clinical decision support. Assists communication only.
- **Not a walled garden.** Patient exports freely. Uses any AI they choose.
- **Not a doctor product.** Doctor receives reports. Does not log in, does not pay (in early phases).
- **Not a replacement for medical records.** Supplements, not substitutes, clinical documentation.
- **Not a diagnostic tool.** Extracts what was discussed. Does not interpret clinical significance.
