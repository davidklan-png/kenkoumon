# Kenkoumon Scenario Evaluation and Testing Strategy

## Executive Summary

This document analyzes the current mock recording scenario coverage, identifies gaps in testing, and provides recommendations for comprehensive testing until the system produces trustworthy results.

**Current Status:** 10 scenarios covering basic consultation types
**Target:** 25+ scenarios covering edge cases, high-risk situations, and diverse patient populations

---

## Current Scenario Coverage Analysis

### Existing Scenarios (10)

| ID | Scenario | Complexity | Duration | Key Topics | Edge Cases |
|----|----------|------------|----------|------------|------------|
| mock_001 | General Health Checkup | Low | 420s | Preventive care, lifestyle | - |
| mock_002 | Diabetes Followup | Medium | 580s | Chronic condition, HbA1c, medication | - |
| mock_003 | Cold/Flu Consultation | Low | 320s | Acute illness, prescriptions | - |
| mock_004 | Polypharmacy Review | High | 650s | Elderly, drug interactions | Multiple medications |
| mock_005 | Specialist Referral | Medium | 480s | Cardiology, angina, referral | - |
| mock_006 | Emergency Brief | Critical | 90s | Chest pain, emergency | Very short + high urgency |
| mock_007 | Pediatric | Medium | 380s | Child patient, asthma | 3 participants (parent present) |
| mock_008 | Mental Health | High | 520s | Depression, suicidal ideation | Sensitive topic |
| mock_009 | Heavy Jargon | High | 450s | Medical terminology | Technical language |
| mock_010 | Elderly/Confusion | High | 580s | Cognitive concerns | Elderly communication |

### Coverage Analysis by Category

#### Medical Specialties Covered
- ✅ General Practice / Internal Medicine
- ✅ Endocrinology (Diabetes)
- ✅ Cardiology (angina, referral)
- ✅ Pediatrics
- ✅ Mental Health

#### Medical Specialties NOT Covered
- ❌ Obstetrics/Gynecology
- ❌ Dermatology
- ❌ Orthopedics
- ❌ Gastroenterology
- ❌ Ophthalmology
- ❌ Urology
- ❌ Surgery (pre/post-op)

#### Consultation Types Covered
- ✅ Routine checkup
- ✅ Chronic condition followup
- ✅ Acute illness
- ✅ Medication review
- ✅ Specialist referral
- ✅ Emergency brief
- ✅ Mental health

#### Consultation Types NOT Covered
- ❌ New medication prescription
- ❌ Surgical consent discussion
- ❌ Lab results disclosure (abnormal)
- ❌ Telephone consultation
- ❌ Dietary/Nutrition counseling
- ❌ Vaccination discussion
- ❌ Hospital discharge planning
- ❌ Cancer diagnosis disclosure

#### Edge Cases Covered
- ✅ Very short consultation (90s)
- ✅ Multi-speaker (pediatric with parent)
- ✅ Sensitive topic (mental health)
- ✅ Heavy medical jargon
- ✅ Elderly patient with cognitive issues

#### Edge Cases NOT Covered
- ❌ Family member as interpreter
- ❌ Professional interpreter present
- ❌ Patient refuses treatment
- ❌ Doctor delivers bad news (cancer, serious illness)
- ❌ Patient non-compliant with treatment
- ❌ Language barrier (non-native speaker)
- ❌ Hearing/speech impaired
- ❌ Angry/agitated patient
- ❌ Doctor interrupted/emergency
- ❌ Multiple family members present
- ❌ Patient asks difficult questions
- ❌ Uncertain diagnosis

#### Safety-Critical Scenarios Covered
- ✅ Emergency identification (chest pain)
- ✅ Suicide risk assessment
- ✅ Polypharmacy safety

#### Safety-Critical Scenarios NOT Covered
- ❌ New medication side effects
- ❌ Allergy identification/documentation
- ❌ Allergy emergency (anaphylaxis)
- ❌ Medication error discovery
- ❌ Surgical risk disclosure
- ❌ Discharge with red flags
- ❌ Warning sign education

---

## Priority Recommendations for New Scenarios

### Critical Priority (Safety-Critical)

These scenarios MUST be implemented before any production use, as failures could result in patient harm.

#### 1. New Medication Prescription (drug_prescription_new)
- **Why Critical:** Patient safety - understanding side effects and proper usage
- **Topics:** Prescription, side_effects, medication_instructions, dosage
- **Edge Cases:** New medication, complex instructions, contraindications
- **Key Elements to Test:**
  - Medication name correctly captured
  - Dosage instructions accurately extracted
  - Side effects documented
  - Warning signs identified

#### 2. Surgical Consent Discussion (surgery_consent)
- **Why Critical:** Legal and safety - requires accurate documentation of risks
- **Topics:** Surgery, informed_consent, risks, recovery_time, complications
- **Edge Cases:** Legal discussion, risk assessment, patient hesitation
- **Key Elements to Test:**
  - Procedure name accurately captured
  - Risks identified and documented
  - Patient questions/concerns captured
  - Follow-up plans clear

#### 3. Hospital Discharge Planning (discharge_planning)
- **Why Critical:** Care transition - high risk of errors and readmission
- **Topics:** Discharge, medications, follow_up, warning_signs, red_flags
- **Edge Cases:** Care transition, multiple medications, patient education
- **Key Elements to Test:**
  - All medications listed correctly
  - Warning signs identified
  - Follow-up appointments captured
  - Activity restrictions documented

#### 4. Allergy Consultation (allergy_consultation)
- **Why Critical:** Anaphylaxis risk - requires accurate allergen identification
- **Topics:** Allergy, anaphylaxis, testing, epipen, avoidance
- **Edge Cases:** Safety critical, emergency medication, allergen identification
- **Key Elements to Test:**
  - All allergens correctly identified
  - Reaction severity documented
  - Emergency plan captured
  - Epipen use instructions

#### 5. Cancer Diagnosis Disclosure (cancer_diagnosis)
- **Why Critical:** High-stakes emotional conversation - accuracy essential
- **Topics:** Cancer, diagnosis, treatment_options, prognosis, staging
- **Edge Cases:** Breaking bad news, emotional support, family presence
- **Key Elements to Test:**
  - Diagnosis type and stage
  - Treatment options presented
  - Patient questions/concerns
  - Emotional state acknowledged

### High Priority (Common Situations)

#### 6. Lab Results - Abnormal (lab_results_abnormal)
- **Why:** High anxiety situations requiring accurate communication
- **Topics:** Lab results, abnormal values, further testing, monitoring
- **Edge Cases:** Anxiety patient, uncertain diagnosis, possible cancer

#### 7. Chronic Pain Management (chronic_pain_management)
- **Why:** Complex condition, opioid safety concerns
- **Topics:** Chronic pain, pain_scale, medication, physical_therapy, opioids
- **Edge Cases:** Subjective symptoms, long-term care, pain medication contracts

#### 8. Medication Side Effect Consultation (medication_side_effect)
- **Why:** Safety critical - requires accurate assessment
- **Topics:** Side_effects, adverse_reaction, medication_change, reporting
- **Edge Cases:** Adverse event, medication adjustment, patient concern

#### 9. Family Present with Interpreter (family_present_interpreter)
- **Why:** Multi-speaker scenario with translation layer
- **Topics:** Family, interpreter, communication_barrier, cultural_considerations
- **Edge Cases:** Multi-speaker, third-party translation, family dynamics
- **Participants:** Doctor, patient, family member, interpreter

#### 10. Dementia Care Planning (dementia_care_planning)
- **Why:** Complex family discussion with legal implications
- **Topics:** Dementia, care_planning, family_discussion, legal, future_planning
- **Edge Cases:** Cognitive decline, family caregiver, legal considerations

### Medium Priority (Important Coverage)

#### 11. Telephone Consultation (telephone_consultation)
- **Topics:** Telephone, triage, home_care_advice
- **Edge Cases:** Audio only, remote assessment, no visual cues

#### 12. Dietary Counseling (dietary_counseling)
- **Topics:** Nutrition, diet, lifestyle_changes, diabetes_diet, restrictions
- **Edge Cases:** Detailed instructions, behavior change

#### 13. Vaccination Discussion (vaccination_discussion)
- **Topics:** Vaccination, side_effects, schedule, hesitancy
- **Edge Cases:** Patient concerns, vaccine hesitancy

#### 14. Pregnancy Checkup (pregnancy_care)
- **Topics:** Pregnancy, prenatal_care, due_date, symptoms, fetal_health
- **Edge Cases:** Obstetrics, fetal health

#### 15. Physical Examination (physical_examination)
- **Topics:** Physical_exam, symptoms, diagnosis, findings
- **Edge Cases:** Procedural language, patient instructions during exam

---

## Testing Strategy Until Results Are Trustworthy

### Phase 1: Baseline Testing (Current State)
- **Goal:** Establish baseline performance metrics
- **Actions:**
  - Run all 10 existing scenarios through the system
  - Document accuracy for each category (chief complaint, findings, recommendations, follow-up)
  - Identify failure modes
- **Success Criteria:** 70%+ overall accuracy across all scenarios

### Phase 2: Critical Scenarios
- **Goal:** Ensure safety-critical scenarios pass
- **Actions:**
  - Implement 5 critical priority scenarios
  - Test to 90%+ accuracy on safety-critical elements
  - Document any failures and iterate
- **Success Criteria:** 90%+ accuracy on safety-critical elements

### Phase 3: High-Priority Coverage
- **Goal:** Cover common high-risk situations
- **Actions:**
  - Implement 5 high-priority scenarios
  - Test to 80%+ overall accuracy
  - Focus on edge cases and complex situations
- **Success Criteria:** 80%+ accuracy on high-priority scenarios

### Phase 4: Comprehensive Coverage
- **Goal:** Broad coverage of medical situations
- **Actions:**
  - Implement remaining medium-priority scenarios
  - Add variations for each scenario type
  - Test with different accents, speech patterns
- **Success Criteria:** 85%+ overall accuracy across all scenarios

### Phase 5: Edge Case Stress Testing
- **Goal:** Ensure robustness in difficult situations
- **Actions:**
  - Create extreme edge cases (overlapping speech, background noise, interruptions)
  - Test with non-standard language patterns
  - Test with emotional speech (crying, angry)
- **Success Criteria:** 75%+ accuracy even on edge cases

---

## Scenario Template for New Tests

```json
{
  "id": "mock_XXX",
  "scenario": "scenario_name",
  "title": "Japanese Title - English Title",
  "language": "ja",
  "duration_seconds": 0,
  "priority": "critical|high|medium|low",
  "complexity": "low|medium|high|critical",
  "edge_cases": ["list", "of", "edge_cases"],
  "safety_critical": true|false,
  "participants": {
    "doctor": {"name": "...", "specialty": "...", "hospital": "..."},
    "patient": {"name": "...", "age": 0, "gender": "..."}
  },
  "transcript": [
    {"speaker": "doctor", "text": "...", "timestamp_start": 0, "timestamp_end": 0}
  ],
  "expected_summary": {
    "chief_complaint": "...",
    "findings": ["..."],
    "recommendations": ["..."],
    "prescriptions": ["..."],
    "follow_up": "...",
    "warnings": ["..."],
    "red_flags": ["..."]
  }
}
```

---

## Success Metrics

### Minimum Thresholds for Production Readiness

| Category | Minimum Accuracy | Target Accuracy |
|----------|------------------|-----------------|
| Chief Complaint | 90% | 95% |
| Findings (Medical) | 85% | 90% |
| Findings (Medications) | 95% | 99% |
| Recommendations | 80% | 90% |
| Follow-up Plans | 90% | 95% |
| Safety Warnings | 95% | 99% |
| Overall | 85% | 90% |

### Testing Protocol

1. **Automated Testing:** Run all scenarios through automated test suite
2. **Manual Review:** Medical professional reviews 20% of outputs
3. **Edge Case Testing:** Monthly testing with new edge cases
4. **Regression Testing:** Full suite run after any model changes
5. **Production Monitoring:** Sample review of real consultations (with consent)

---

## Next Steps

1. ✅ Run existing 10 scenarios through system (baseline)
2. 🔲 Implement 5 critical priority scenarios
3. 🔲 Test with local LLM (Ollama) to establish baseline
4. 🔲 Test with cloud LLM for comparison
5. 🔲 Iterate on prompts based on failures
6. 🔲 Expand to high-priority scenarios
7. 🔲 Achieve 85%+ accuracy across all scenarios
8. 🔲 Conduct real-world pilot testing

---

## Scenario Parameters for Comprehensive Testing

### Variations to Include

For each scenario type, create variations with:
- **Patient Age:** Pediatric (0-14), Adult (15-64), Geriatric (65+)
- **Gender:** Male, Female, Non-binary
- **Speech Style:** Fast talker, slow talker, mumbler, emotional
- **Consultation Length:** Very short (<2 min), average (5-10 min), long (>15 min)
- **Number of Speakers:** 1-on-1, with family member, with interpreter
- **Emotional State:** Calm, anxious, angry, crying, confused
- **Medical Complexity:** Simple, moderate, highly technical
- **Outcome:** Clear diagnosis, uncertain diagnosis, referral needed

### Audio Quality Variations

- Clear studio quality
- Background noise (hospital environment)
- Telephone quality
- Overlapping speech (interruptions)
- Quiet speaker
- Fast speaker
- Non-native accent

---

## Conclusion

Current scenario coverage provides a foundation but is insufficient for production use. The system must be tested against at least 25+ scenarios covering critical safety situations, edge cases, and diverse patient populations before results can be considered trustworthy.

**Recommended Testing Sequence:**
1. Baseline with current 10 scenarios
2. Add 5 critical safety scenarios
3. Add 5 high-priority scenarios
4. Add remaining medium-priority scenarios
5. Stress test with extreme edge cases

**Estimated Time to Trustworthiness:** 3-6 months of iterative testing and refinement, assuming access to quality Japanese LLM and appropriate medical domain fine-tuning.
