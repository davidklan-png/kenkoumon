# Kenkoumon Experiment Zero - Self-Evaluation Scorecard

**Session ID:** YYYY-MM-DD-doctor
**Date of Visit:** YYYY-MM-DD
**Doctor/Specialty:** _____________________
**Transcription Source:** [ ] On-device [ ] User-hosted [ ] Cloud API
**Report Generation Source:** [ ] On-device [ ] User-hosted [ ] Cloud API

---

## Part 1: Transcription Quality (1-10)

| Criterion | Score (1-10) | Notes |
|-----------|--------------|-------|
| Overall transcription accuracy | ___/10 | |
| Medical terminology accuracy | ___/10 | List any missed/misheard terms: |
| Japanese readability | ___/10 | Any grammatical issues or nonsensical passages? |

**Transcription Issues:**
- Medications missed or misspelled:
- Conditions/procedures missed:
- Other errors:

---

## Part 2: Report Section Quality (1-10 each)

### Section 1: 診察内容の要約 (Visit Summary)
**Score:** ___/10

**Issues:**
- Missing key information:
- Incorrect information:
- Japanese register concerns (too casual/too formal):

### Section 2: 主な医療情報 (Key Medical Information)
**Score:** ___/10

**Entity Extraction Quality:**
| Entity Type | Extracted Correctly | Issues |
|-------------|---------------------|--------|
| Medications | [ ] Yes [ ] Partial [ ] No | |
| Conditions | [ ] Yes [ ] Partial [ ] No | |
| Instructions | [ ] Yes [ ] Partial [ ] No | |
| Providers | [ ] Yes [ ] Partial [ ] No | |

**Specific Issues:**

### Section 3: 次回診察に向けて (Next Visit Prep)
**Score:** ___/10

**Observation Quality:**
- [ ] Actionable items for next visit included?
- [ ] Appropriate (not clinical advice, just observations)?
- [ ] Missing context that would be useful?

**Issues:**

### Section 4: 患者からのメモ (Patient Notes)
**Score:** N/A (filled by patient)

---

## Part 3: Overall Assessment

### Accuracy Assessment
**Overall Accuracy:** ___/10

**Critical Errors:** (Any wrong medications, dosages, or instructions?)
- [ ] No critical errors
- [ ] Critical errors found (describe below):

**Description of Critical Errors:**

---

### Usefulness Assessment
**Would this report be useful to a doctor?**
- [ ] Very useful (9-10)
- [ ] Somewhat useful (7-8)
- [ ] Neutral (5-6)
- [ ] Not very useful (3-4)
- [ ] Not useful at all (1-2)

**What would make it more useful?**

---

### Decision Gate
**Outcome:**
- [ ] **Accurate + Useful** → Proceed to expanded validation
- [ ] **Accurate + Not Useful** → Redesign report format
- [ ] **Not Accurate** → Investigate (transcription vs. report generation)

**Notes on Decision:**

---

## Part 4: Technical Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Audio duration | ___ minutes | |
| Transcription time | ___ seconds | |
| Report generation time | ___ seconds | |
| Total processing time | ___ minutes | |
| Device used | _____________________ | |
| Battery impact | [ ] Low [ ] Medium [ ] High | |

---

## Part 5: Doctor Feedback (To be filled at next visit)

**Did the doctor review the report?** [ ] Yes [ ] No

**Doctor's Response:**
- [ ] Found it accurate
- [ ] Found it useful
- [ ] Would want to receive these regularly
- [ ] Had concerns or suggestions

**Doctor Comments:**

**Go/No-Go for Expanded Validation:**
- [ ] Go (proceed to 5-user validation)
- [ ] Conditional go (changes needed first)
- [ ] No-go (major redesign needed)

---

## Part 6: Prompt Tuning Notes

**Transcription Issues for Fine-Tuning:**

**Report Generation Issues for Prompt Adjustment:**

**Japanese Register Feedback:**

**Other Observations:**

---

**Scorecard Completed By:** _____________________
**Date Completed:** YYYY-MM-DD
