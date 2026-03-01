# Kenkoumon — Risk Register

## Critical Risks (Could Kill the Business)

### RISK-1: Doctor Resistance to Recording

**Severity:** High
**Likelihood:** Medium-High
**Phase:** All phases

**Description:** Doctors refuse to be recorded, either due to personal discomfort, clinic policy, or medical association guidance. If patients can't record, there is no product.

**Signals:**
- >30% of patients report their doctor refused recording
- Medical associations issue guidance against patient recording
- Clinics institute blanket no-recording policies

**Mitigation:**
- Design a consent moment that frames recording as mutual benefit (deferred, Decision 9)
- Provide patients with a script and optional printed card
- Target clinics that already embrace patient experience innovation
- Consider alternative: patient dictates their own post-visit recall instead of recording (degraded but functional)

**Kill criteria:** If >50% of target patients cannot get recording consent after consent flow optimization, pivot to post-visit patient recall model.

---

### RISK-2: Transcription Accuracy Insufficient for Medical Japanese

**Severity:** High
**Likelihood:** Medium

**Description:** Japanese medical consultations involve specialized terminology, mumbling, cross-talk, and variable audio quality in clinic environments. Current transcription models may not achieve sufficient accuracy for medical entity extraction.

**Signals:**
- Medication names consistently misspelled or missed
- Key instructions lost or garbled
- Accuracy below 80% on medical terms across multiple recordings

**Mitigation:**
- Test multiple transcription services/models during Experiment Zero
- Japanese-specialized models exist (e.g., ReazonSpeech) — evaluate alternatives to Whisper
- Fine-tuning on medical Japanese audio is possible with sufficient data
- Post-processing correction layer using medical terminology dictionaries

**Kill criteria:** If no available transcription solution achieves >85% accuracy on medical terms after optimization, the recording-based approach may not be viable. Consider: manual transcript correction by patient as interim step.

---

### RISK-3: AI Misinterprets Conversation — Doctor Acts on Bad Information

**Severity:** Critical (reputational and safety)
**Likelihood:** Low-Medium

**Description:** The AI generates a report that contains factually incorrect medical information (wrong medication, wrong dosage, wrong instruction). The doctor reads it and it influences their care decisions, potentially causing patient harm.

**Signals:**
- Any instance of a wrong medication name or dosage in a generated report
- Doctor reports acting on information from the report that was inaccurate
- Pattern of subtle errors (e.g., omitting "do not" from instructions)

**Mitigation:**
- Wellness tool positioning: disclaimer clearly states the doctor must verify all content (legal protection)
- Patient review step: patient catches errors before sharing (workflow protection)
- Report framing: presents extracted information, not directives (design protection)
- Section 3 uses observation language, not clinical language (interpretation protection)
- Future: confidence scoring on extracted entities, flagging uncertain items

**Kill criteria:** Any serious adverse event traceable to report inaccuracy. This is an absolute boundary.

---

## Significant Risks (Could Slow or Damage the Business)

### RISK-4: Nobody Pays ¥1,500/Month

**Severity:** High
**Likelihood:** Medium

**Description:** The product is valued as "nice to have" but not enough to sustain a subscription. Expats may use it occasionally but not monthly.

**Signals:**
- Free-to-paid conversion below 10%
- Monthly churn above 30%
- Users say "I'd use it for important appointments but not regular checkups"

**Mitigation:**
- Longitudinal profile creates compounding value (more visits = more useful)
- Document ingestion (kenkou shindan, blood tests) adds value between visits
- Per-session pricing as fallback if subscription doesn't work
- Freemium model: 1 session free, subscription for unlimited

**Pivot option:** If subscription fails, test per-session pricing (¥500-1,000/session). If that fails, explore clinic-pays model (B2B).

---

### RISK-5: APPI Compliance Blocks Production Launch

**Severity:** High
**Likelihood:** Medium

**Description:** Japan's Act on the Protection of Personal Information (APPI), as amended in 2022, has strict requirements for medical data handling. Audio recordings of medical consultations are among the most sensitive data categories. Compliance requirements may be more onerous than anticipated.

**Signals:**
- Legal counsel advises that the data handling approach requires significant restructuring
- Data residency requirements eliminate preferred cloud providers
- Consent requirements exceed what the simple verbal approach supports

**Mitigation:**
- Get preliminary legal opinion early (¥200-500K investment) — recommended in 30-day validation
- Use Japan-region cloud services from day one (Azure Japan East, AWS Tokyo)
- Patient-owned data model aligns with APPI's direction toward individual data rights
- Audio deletion after transcription reduces exposure

**Contingency:** If APPI requirements are prohibitive for cloud processing, accelerate on-device transcription roadmap.

---

### RISK-6: Competitor Adds This Feature

**Severity:** Medium
**Likelihood:** Medium (12-24 month horizon)

**Description:** Nuance DAX, Abridge, or a major tech company (Google Health, Apple) adds multilingual transcription and patient-facing summaries to their existing clinical AI products.

**Signals:**
- Major competitor announces multilingual patient summary feature
- Japanese market entry by existing clinical AI company

**Mitigation:**
- Patient-owned longitudinal profile is the moat, not the transcription or report generation
- Competitors are doctor-facing (B2B enterprise sales). Kenkoumon is patient-facing (B2C). Different buyer, different sales motion, different product philosophy.
- Open export format creates ecosystem lock-in that proprietary platforms can't match
- Japanese market expertise and bilingual entity database are hard to replicate quickly

**Assessment:** This risk is real but the competitive response would likely be a doctor-facing feature added to existing products, not a patient-owned platform. Different product for a different user.

---

### RISK-7: Patient Workflow Dropout

**Severity:** Medium-High
**Likelihood:** Medium

**Description:** The patient-driven workflow has multiple steps: record → upload → wait → review → add notes → share. Each step is a dropout point. Patients may find the process too cumbersome compared to "just going to the doctor."

**Signals:**
- >40% of recordings never get processed
- >50% of processed reports never get shared
- Users describe the process as "too much work"

**Mitigation:**
- "Process and send immediately" option reduces steps to: record → confirm → done
- Make the default path as frictionless as possible (one-tap processing after recording stops)
- Patient notes section is optional, not blocking
- Push notifications to remind about unprocessed recordings

**Design principle:** The minimum viable workflow is: stop recording → tap "process and share" → done. Everything else (review, notes, deferred sharing) is optional enhancement.

---

## Monitoring Risks (Watch but Don't Act Yet)

### RISK-8: Medical Association Backlash

**Likelihood:** Low in Japan (patient recording is culturally less confrontational than in US)
**Trigger:** Media coverage of AI-generated medical reports causing concern among physician groups
**Action if triggered:** Proactive engagement with medical associations. Frame as patient communication tool, not clinical oversight.

### RISK-9: Audio Quality in Clinic Environments

**Likelihood:** Medium
**Trigger:** Consistent transcription failures due to background noise, distance from doctor, air conditioning, etc.
**Action if triggered:** Provide recording best practices in-app. Test external microphone recommendations. Consider noise-reduction preprocessing.

### RISK-10: Cultural Resistance from Japanese Patients (Expansion Risk)

**Likelihood:** Medium (for expansion beyond expats to Japanese patients)
**Trigger:** Japanese patients express discomfort with recording or AI analysis of medical conversations
**Action if triggered:** This is a Phase 3+ concern. Expat market doesn't have this risk. Reassess when expanding to domestic Japanese users.

---

## Risk Review Schedule

| Milestone | Risks to Reassess |
|---|---|
| After Experiment Zero | RISK-2 (transcription accuracy), RISK-3 (report accuracy) |
| After 5-user validation | RISK-1 (doctor resistance), RISK-7 (workflow dropout) |
| Before MVP launch | RISK-5 (APPI compliance) |
| At 50 subscribers | RISK-4 (willingness to pay), RISK-7 (workflow dropout) |
| At 12 months | RISK-6 (competitive response), RISK-8 (medical association) |
