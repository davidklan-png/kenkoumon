# Doctor Report Specification — V0

## Design Principles
1. Clinically useful, not clinically authoritative
2. Observation over interpretation
3. Appropriate medical Japanese
4. Concise (scannable in 2-3 minutes)

## Report Structure

### Header
- 診察日, 患者名, 担当医, 生成日

### Section 1: 診察内容の要約 (Visit Summary)
- 2-3 paragraphs, narrative, chronological, factual, clinical tone, third-person

### Section 2: 主な医療情報 (Key Medical Information)
- **症状・主訴** — symptoms/complaints discussed
- **診断・評価** — diagnosis or assessment stated
- **処方・治療** — medications (name, dosage, frequency, duration), changes, non-pharma
- **検査** — tests performed, ordered, or results discussed
- **指示事項** — lifestyle, medication instructions, warning signs, follow-up timing

### Section 3: 次回診察に向けて (For the Next Visit)
Observations from conversation to help doctor prepare. All framed as observations:
- ✅ 「患者は薬の副作用について2回質問した」
- ✅ 「患者は食事制限について追加の説明を求める可能性がある」
- ❌ 「患者は健康不安症の兆候を示している」(never use clinical assessments)
- ❌ 「患者の健康リテラシーが低い」(never use judgments)

### Section 4: 患者からのメモ (Patient Notes)
- Blank — patient fills in after reviewing

### Footer
- Disclaimer: AI-generated from audio recording, not a medical record, verify with physician

## Quality Criteria
- Medical terms: >95% accuracy
- Medications/dosages: 100% accuracy (zero tolerance)
- No fabrication beyond conversation content
- Section 3 observations traceable to specific moments
- Total length: 1-2 pages
