# Kenkoumon — Risk Assessment

## Critical Risks (Could Kill the Business)

### Risk 1: Doctor Resistance to Recording
- **Probability:** Medium-High
- **Impact:** Fatal — no recording means no product
- **Description:** Doctors may refuse recording, feel surveilled, or change their behavior when recorded. Some clinics may have explicit no-recording policies. In Japanese medical culture, the power dynamic traditionally favors the physician, and recording may feel like a challenge to that dynamic.
- **Mitigation:**
  - Design a respectful consent flow that frames recording as a patient comprehension aid, not surveillance
  - Provide a suggested script in Japanese that doctors find non-threatening
  - Start with doctors who already serve international patients (accustomed to communication challenges)
  - The doctor report itself is the mitigation — when doctors see the output benefits them, resistance drops
- **Early warning signal:** >30% of doctors refuse recording during Experiment Zero / validation phase
- **Kill trigger:** If the majority of doctors refuse even after seeing the report value, the recording-based model doesn't work in Japan

### Risk 2: Transcription Accuracy for Medical Japanese
- **Probability:** Medium
- **Impact:** High — inaccurate transcription produces dangerous reports
- **Description:** Medical Japanese contains specialized terminology, mixed with casual patient language. Doctors may use technical terms, abbreviations, or speak quickly. Patient speech may include dialectal variations or non-native Japanese. Current ASR models may not reliably handle this mix.
- **Mitigation:**
  - Test transcription accuracy explicitly during Experiment Zero
  - Use the largest available Whisper model (large-v3) for Japanese
  - Consider Japanese-specialized ASR services if Whisper accuracy is insufficient
  - Implement a patient review step where obvious errors can be caught before sharing
  - Long-term: fine-tune transcription models on medical Japanese audio
- **Early warning signal:** Medical term accuracy below 90% during testing
- **Kill trigger:** If transcription cannot reliably capture medication names and dosages after trying multiple approaches, the audio-based pipeline is not viable

### Risk 3: Patients Won't Pay / Won't Use Regularly
- **Probability:** Medium
- **Impact:** Fatal — no revenue, no business
- **Description:** Even if the technology works and doctors like the reports, patients may not value the output enough to pay ¥1,500/month. The workflow requires patient effort (recording, reviewing, sharing). Expats in Japan may see doctors infrequently. The habit loop may not form.
- **Mitigation:**
  - Validate willingness to pay before building (Experiment Zero includes this check)
  - Free first session to prove value
  - Longitudinal profile increases value over time (Stage 3)
  - Document ingestion expands use beyond just visit recordings (Stage 4)
  - Target users with frequent medical visits (chronic conditions, pregnancy, elderly care)
- **Early warning signal:** <50% of Experiment Zero participants say they'd pay
- **Kill trigger:** If after 3 months of available product, monthly active usage is below 20% of subscribers

---

## Serious Risks (Could Significantly Harm the Business)

### Risk 4: AI Misrepresentation in Reports
- **Probability:** Medium
- **Impact:** High — loss of trust, potential harm
- **Description:** The AI may misextract information (wrong medication name, wrong dosage, fabricated instruction) or Section 3 observations may be wrong or offensive. One bad report shown to a doctor could poison the relationship.
- **Mitigation:**
  - Mandatory disclaimer on every report
  - Patient review step before sharing
  - Conservative extraction (better to miss something than fabricate)
  - Section 3 framed as observations, not assessments
  - Quality criteria in DOCTOR-REPORT-SPEC.md: zero tolerance for medication/dosage errors
- **Early warning signal:** Any medication or dosage error in testing

### Risk 5: Regulatory Reclassification
- **Probability:** Low-Medium
- **Impact:** High — could require 12-24 month approval process
- **Description:** Although positioned as a wellness/communication tool, regulators (PMDA, future markets' equivalents) could decide the product qualifies as SaMD if it influences clinical decisions. Risk increases as the interpretation layer deepens in future versions.
- **Mitigation:**
  - Maintain wellness-tool positioning in all materials and outputs
  - Doctor reports include explicit disclaimers
  - Section 3 uses observation framing, never clinical assessment
  - Get preliminary legal opinion during validation phase
  - Monitor regulatory developments in digital health
- **Early warning signal:** Legal counsel advises classification risk is non-trivial

### Risk 6: Data Breach or Privacy Incident
- **Probability:** Low (if designed correctly)
- **Impact:** Critical — medical data breach is reputationally fatal
- **Description:** Medical conversation recordings are extremely sensitive. A breach would destroy trust and likely end the business. Even a perceived privacy risk could prevent adoption.
- **Mitigation:**
  - Encryption at rest and in transit for all data
  - Japan-region data residency for production
  - Patient-controlled deletion (including audio destruction after transcription)
  - Minimize data retention — don't keep what you don't need
  - Security audit before public launch
- **Early warning signal:** Any unauthorized access during development

### Risk 7: Competitor Entry
- **Probability:** Medium (12-24 month horizon)
- **Impact:** Medium — depends on execution speed
- **Description:** If the concept proves viable, larger players (Nuance, Google Health, Apple) could add similar features. Japanese healthcare IT companies could build local alternatives.
- **Mitigation:**
  - Patient-owned longitudinal data creates switching costs
  - Bilingual medical entity database becomes proprietary asset
  - Speed to market in Japan before US competitors localize
  - Network effects if patients bring the product to new doctors
  - Export-first philosophy builds trust that walled-garden competitors won't match
- **Early warning signal:** Major player announces similar product for Japanese market

---

## Moderate Risks (Manageable but Require Attention)

### Risk 8: Japanese Language/Cultural Nuance
- **Description:** Medical Japanese has layers of indirectness and politeness that AI may not interpret correctly. A doctor saying 「ちょっと気になりますね」 (that's a bit concerning) may be communicating significant worry in clinical context. Cultural nuances in doctor-patient communication may be lost or misrepresented.
- **Mitigation:** Prompt engineering specific to Japanese medical communication norms. Test with Japanese-fluent medical professionals. Iterate based on feedback.

### Risk 9: Expat Market Size Ceiling
- **Description:** 3M+ foreign residents in Japan sounds large, but those who see doctors regularly, speak English, and would pay for a health app is a much smaller number. The addressable market for V1 may be smaller than needed.
- **Mitigation:** Expand to Japanese-speaking users once bilingual pipeline proves reliable. Japanese patients who want better communication with specialists or who travel for healthcare are a much larger market.

### Risk 10: Multi-Specialty Variability
- **Description:** A general checkup conversation is different from an oncology consultation, a psychiatric session, or a dental visit. The prompt and extraction logic may not generalize well across specialties.
- **Mitigation:** Start with general internal medicine (most common expat visit type). Expand specialty support deliberately with specialty-specific prompt tuning.

---

## Risk Monitoring Cadence

| Phase | Review Frequency | Key Metrics |
|---|---|---|
| Experiment Zero | After each test | Transcription accuracy, report quality, doctor reaction |
| Validation | Weekly | Consent rates, willingness to pay, accuracy patterns |
| MVP | Bi-weekly | Active users, processing completion rate, sharing rate, retention |
| Growth | Monthly | MRR, churn, NPS, doctor adoption signal |
