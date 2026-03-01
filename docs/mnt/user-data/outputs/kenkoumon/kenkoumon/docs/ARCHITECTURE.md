# Kenkoumon — Architecture Decision Record

This document captures every architectural decision made during the design phase, its rationale, alternatives considered, and impact on future development. Decisions are numbered chronologically and grouped by domain.

---

## Foundational Positioning

### Decision 1: Medical Device or Wellness Tool

**Decision:** Wellness tool.

**Rationale:** The product is completely under the patient's control and is only used to assist the doctor by providing valuable insight into the patient's needs. The patient initiates recording, controls processing, and chooses what to share. The doctor receives information and exercises independent clinical judgment.

**Implications:**
- Likely avoids PMDA (Japan) and FDA classification as Software as a Medical Device (SaMD)
- No regulatory approval process required before selling
- Lower liability exposure — the doctor interprets all outputs at their own discretion
- Same legal relationship as a patient bringing printed health information to a visit
- Cannot market as clinical decision support; must stay within communication/understanding framing

**Trade-off:** Lower regulatory barrier but also lower pricing power compared to certified clinical tools. Acceptable for market entry.

---

## Data Ownership & Architecture

### Decision 2: Data Ownership — Who Owns What

**Decision:** The patient has full control over what is shared with the doctor. The doctor interprets results at their discretion.

**Rationale:** Patient-centric data ownership aligns with the regulatory direction of Japan's APPI (amended 2022), creates the foundation for a portable health profile, and avoids building a B2B product before validating core value.

**Implications:**
- The patient is the data controller under APPI
- No clinic-side data agreements needed for v1
- Doctor never logs into the platform — receives shared outputs only
- Consent model is simpler: patient consents to their own recording and processing
- Network effects become possible when patients carry profiles between providers

### Decision 7: Patient Identity and Profile Continuity

**Decision:** Longitudinal profile. The overall objective is to give patients 100% control over their entire health data including biometric trackers, phone health data, and all medical records. A complete silo of the patient's entire health history, shareable with their preferred AI and doctors.

**Rationale:** This is the long-term vision that differentiates Kenkoumon from a simple transcription tool. However, this expands scope significantly beyond a visit recording product into a personal health data platform.

**Implications:**
- Must design the data model for longitudinal accumulation from day one, even if v1 only fills in visit data
- Creates subscription value (data compounds over time)
- Positions the company as health data infrastructure, not health AI
- Requires entity-centric data model (see Decision 12)
- Competes long-term with Apple Health, Google Health, and PHR platforms — but with a stronger wedge (visit intelligence)

**Critical constraint:** The longitudinal vision must not delay the Experiment Zero validation. Build the skeleton for longitudinal; populate only visit data initially.

### Decision 12: Data Model — Session-Centric vs. Entity-Centric

**Decision:** Entity-centric.

**Rationale:** An entity-centric model extracts discrete medical entities (conditions, medications, providers, vitals, instructions) as independent objects with their own lifecycle, rather than trapping everything inside session transcripts. This supports the longitudinal profile vision and makes future data sources (wearables, lab imports, document scans) first-class citizens.

**Implications:**
- Each entity (medication, condition, provider, etc.) has a canonical ID, source reference, timestamp, and bilingual labels
- The data model has slots for future data sources (biometrics, lab results, imaging) even if they're empty in v1
- More upfront data modeling work (estimated 2-3 extra weeks) but avoids full re-architecture later
- Enables future AI querying: every entity is individually addressable and traceable to its source

**Target entity model (v1 populated entities marked with check):**
```
Patient
├── Providers         ✓ (extracted from visit recordings)
├── Conditions        ✓ (extracted from visit recordings)
├── Medications       ✓ (extracted from visit recordings)
├── Instructions      ✓ (extracted from visit recordings)
├── Sessions          ✓ (visit recordings and generated reports)
├── Biometrics        ○ (future: wearables, phone health data)
├── Lab Results       ○ (future: blood tests, kenkou shindan)
├── Documents         ○ (future: imported PDFs, images, scans)
└── Imaging           ○ (future: DICOM files)
```

---

## AI & Processing

### Decision 3: Build vs. Buy the AI Stack

**Decision:** Run POC with available technology. Adjust based on privacy laws and data residency requirements.

**Rationale:** Bootstrap the experiment with existing APIs (Whisper for transcription, Claude/GPT-4 for extraction and report generation). Defer proprietary model investment until the core hypothesis is validated and data residency requirements are fully understood.

**Implications:**
- POC can run with zero ML infrastructure — API calls only
- Must use services with Japan-region deployment for production (Azure OpenAI Japan East, AWS Bedrock Tokyo)
- Abstract the AI layer so providers can be swapped without re-architecture
- Plan migration to fine-tuned models within 12-18 months as training data accumulates
- Data residency under APPI is non-negotiable for production; acceptable risk for personal POC

### Decision 4: Real-Time vs. Post-Visit Processing

**Decision:** Patient chooses when visit data gets processed and released. Two modes:
1. **Immediate processing:** Patient confirms to process and sends without review
2. **Deferred processing:** Patient processes later, reviews the output, adds personal comments, then shares

**Rationale:** Reflects the patient-owned philosophy. The patient controls the entire workflow timeline. Post-visit processing is simpler technically, allows higher accuracy (multiple analysis passes), and avoids workflow disruption during the consultation.

**Implications:**
- No real-time requirements in v1 (dramatically reduces technical complexity)
- The patient's review-and-annotate step adds unique value to the report
- Latency is not a critical metric — minutes to hours of processing time is acceptable
- UX must clearly present both processing modes without making the flow confusing

### Decision 13: AI Role — Extraction vs. Interpretation

**Decision:** V1 does extraction plus one layer of interpretation: communication preferences and emotional tone. No clinical interpretation.

**Rationale:** Extraction (what was said) is verifiable and safe. Light interpretation (patient seemed hesitant about medication, patient returned to side effects topic multiple times) adds unique value without crossing into clinical assessment territory.

**Implications:**
- Report frames observations as patient behavior, not clinical assessments
- "Patient asked three questions about side effects" (extraction) ✓
- "Patient may want more detailed information about medication risks" (light interpretation) ✓
- "Patient has health anxiety" (clinical interpretation) ✗ — not in v1
- Each expansion of the interpretation layer is a deliberate product decision with its own validation

---

## Language & Localization

### Decision 11: Localization Strategy

**Decision:** Japanese-first. The core user is an English speaker with Japanese doctors. The product is a go-to app for expats or tourists in Japan.

**Rationale:** ~3 million foreign residents in Japan face a language and cultural communication gap in healthcare. The pain is acute, willingness to pay is high, and it sidesteps the "why do I need this?" objection from patients who understood the conversation. The language barrier itself is a competitive moat against US-based clinical AI tools.

**Implications:**
- Input: Japanese audio (doctor speaks Japanese)
- Output v1: Japanese doctor briefing (for the doctor)
- Output v2: English patient summary (for the patient) — deferred until after Experiment Zero
- Product marketing and onboarding in English, targeting expat communities
- Natural expansion path: medical tourism, expat clinics across Asia, Korean/Chinese language support

### Decision 14: Language Architecture

**Decision:** Transcribe in source language (Japanese). Maintain bilingual entity mappings.

**Rationale:** Preserving medical Japanese terminology during transcription maintains clinical precision. Bilingual entity mappings (e.g., アムロジピン ↔ Amlodipine) enable accurate cross-language outputs and future multilingual support.

**Implications:**
- Entity model requires a localization layer: each medication, condition, and procedure has a canonical ID with names in each supported language
- Medical terminology databases (MedDRA, available in Japanese) bootstrap the bilingual mappings
- Transcription → extraction happens in Japanese; translation occurs at the output generation layer
- This is core product differentiation, not a nice-to-have

---

## Product & Delivery

### Decision 5: Single Buyer vs. Two-Sided

**Decision:** Eventually two-sided, defer for now.

**Rationale:** The product starts as a patient tool. The patient records, processes, and shares. No clinic-side product, no enterprise sales, no doctor portal. Two-sided dynamics (patient pulls product into new clinics, clinics see value and subscribe) emerge naturally once the patient-side product is proven.

### Decision 6: Delivery Mechanism to the Doctor

**Decision:** Secure link. (As recommended.)

**Rationale:** The patient generates a secure link to the doctor's briefing report and shares it however they want — email, LINE message, printed QR code handed to reception. No clinic-side integration, no app install, no portal.

**Implications:**
- Zero friction for clinics — nothing to install or learn
- Anonymous analytics possible (was the link opened?)
- No visibility into whether doctor actually read vs. skimmed
- Can layer a clinic portal on top later; cannot un-build one shipped too early
- Link expiration and access controls needed for PHI protection

### Decision 8: The Recording Itself

**Decision:** Patient-controlled technology. Bootstrap for POC and figure out privacy details later.

**Rationale:** For Experiment Zero, the patient uses whatever recording method they have (phone's built-in recorder, a simple app). No custom recording infrastructure. Privacy and data handling details are deferred to the productization phase.

**Implications for future:**
- Production app will need: encryption at rest, controlled upload flow, patient-controlled deletion
- Raw audio is the most sensitive data category — long-term roadmap should include on-device transcription to eliminate audio transit
- APPI compliance for audio storage must be resolved before production launch

### Decision 9: Consent Flow

**Decision:** Deferred.

**Rationale:** For Experiment Zero, the patient simply asks the doctor for verbal permission to record. Designed consent flows (scripts, cards, in-app guidance) are a product design problem to solve after validation.

**Note:** This remains a high-impact decision. Doctor resistance to recording is one of the top risks. Should be addressed before scaling beyond personal use.

### Decision 10: Report Content

**Decision:** Start with the basics. What the doctor can use for notes, preparation for the next visit, and maintaining a comprehensive understanding of the patient.

**Rationale:** The report should be immediately useful within a doctor's existing workflow — supplementing their notes, preparing for follow-ups, and capturing information they may not have had time to document.

**Report structure defined in [REPORT-TEMPLATE.md](REPORT-TEMPLATE.md):**
1. 診察内容の要約 (Visit Summary)
2. 主な医療情報 (Key Medical Information) — structured extraction
3. 次回診察に向けて (For the Next Visit) — observations for follow-up
4. 患者からのメモ (Patient Notes) — patient's own additions
5. Disclaimer footer

---

## Data Export & Privacy

### Decision 15: "Share With My AI"

**Decision:** The patient dumps their health data (kenkou shindan, reports, images, blood tests) into a folder and uses whatever AI they prefer — subscription service, local LLM, any tool. The system must educate patients on PHI privacy risks depending on which AI they choose.

**Rationale:** No vendor lock-in. No proprietary AI query layer. The patient exports structured data and chooses their own AI. This is philosophically radical (most health platforms build walled gardens) but creates zero adoption friction, compatibility with the entire AI ecosystem, and attracts privacy-conscious users.

**Implications:**
- Kenkoumon's value is in collection, structuring, and maintenance of health data — not in the AI that reads it
- Business model must be based on the pipeline (recording → structuring → maintaining), not on AI insights
- Export format becomes a critical product decision (deferred, see Decision 16)
- PHI risk education is a product responsibility (see Decision 18)

### Decision 16: Export Format

**Decision:** Deferred until MVP is complete.

**Rationale:** The export format is important for ecosystem compatibility but is not needed for Experiment Zero or initial MVP. The user dumps data in many formats and expects it to be processed. Format standardization happens after the core product is validated.

**Note:** This decision has high future impact. If the export format becomes a de facto standard, it creates an ecosystem moat. Should be revisited immediately post-MVP.

### Decision 17: Document Ingestion

**Decision:** Deferred until MVP is complete. User dumps data in many formats and expects it to be processed.

**Rationale:** Building ingestion pipelines for kenkou shindan, blood tests, prescriptions, and other Japanese health documents is tractable but not needed for Experiment Zero. The AI processing of diverse document formats is a v2+ feature.

### Decision 18: PHI Risk Communication

**Decision:** Tiered export. User must be educated on their privacy considerations.

**Rationale:** Different AI providers have different data handling practices. The patient must understand the trade-offs before sharing health data with any AI service.

**Implementation (post-MVP):**
- **Full export** — all data, for use with local LLMs or trusted infrastructure
- **De-identified export** — provider names replaced, dates shifted, clinic names removed. Medical content preserved. Safe for cloud AI services.
- Every export includes a PRIVACY-WARNING file explaining PHI risks per AI provider category
- In-app education on data residency, training data policies, and cross-border transfer risks

---

## Validation

### Decision 19: MVP Scope Lock

**Decision:** First visit only. Record the conversation, immediately process, and produce a report for the doctor to review in Japanese. Based on that result, decide next steps.

**Rationale:** Maximum scope reduction. One recording, one processing run, one report. If the output isn't good enough for a doctor to find useful, nothing else matters. This can be validated in a single day with zero infrastructure.

### Decision 20: Doctor Report Content Structure

**Decision:** Four-section Japanese-language report designed for physician review.

**Structure:**
1. **診察内容の要約** — Narrative visit summary
2. **主な医療情報** — Structured extraction (symptoms, diagnosis, medications, tests, instructions)
3. **次回診察に向けて** — Observations for next visit (topics to revisit, apparent patient questions, areas needing clarification)
4. **患者からのメモ** — Blank section for patient's own comments

**Full template and generation prompt in [REPORT-TEMPLATE.md](REPORT-TEMPLATE.md).**

---

## Decision Status Summary

| # | Decision | Status | Reversibility |
|---|---|---|---|
| 1 | Wellness tool positioning | ✅ Decided | Low — changes regulatory path |
| 2 | Patient owns all data | ✅ Decided | Low — changes entire architecture |
| 3 | Buy/API for POC | ✅ Decided | High — can migrate later |
| 4 | Post-visit, patient-controlled timing | ✅ Decided | Medium |
| 5 | Defer two-sided market | ✅ Decided | High — revisit post-validation |
| 6 | Secure link delivery | ✅ Decided | High — can add portal later |
| 7 | Longitudinal profile (vision) | ✅ Decided | Low — defines data architecture |
| 8 | Patient's own device for recording | ✅ Decided | High — bootstrap for POC |
| 9 | Consent flow | ⏸️ Deferred | — |
| 10 | Doctor-useful report basics | ✅ Decided | Medium |
| 11 | Japanese-first, expat market | ✅ Decided | Medium — defines go-to-market |
| 12 | Entity-centric data model | ✅ Decided | Low — defines data layer |
| 13 | Extraction + light interpretation | ✅ Decided | Medium — can expand carefully |
| 14 | Source-language transcription, bilingual entities | ✅ Decided | Low — core architecture |
| 15 | Open export, patient chooses AI | ✅ Decided | Low — defines business model |
| 16 | Export format | ⏸️ Deferred | — |
| 17 | Document ingestion | ⏸️ Deferred | — |
| 18 | Tiered export with PHI education | ✅ Decided | Medium |
| 19 | MVP = one visit, one report | ✅ Decided | High — scope gate |
| 20 | Four-section Japanese doctor report | ✅ Decided | High — iterate on content |
