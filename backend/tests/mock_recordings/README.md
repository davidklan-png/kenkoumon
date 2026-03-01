# Mock Doctor-Patient Recordings (Japanese)

Test data for Kenkoumon audio transcription and summary generation.

## Overview

This directory contains mock Japanese doctor-patient conversation transcripts
for testing the Kenkoumon system's transcription and AI summarization capabilities.

## Scenarios

| ID | Scenario | Title | Duration | Focus |
|----|----------|-------|----------|-------|
| mock_001 | general_checkup | 一般健康診断 | 7 min | Preventive care, lifestyle advice |
| mock_002 | chronic_condition_followup | 糖尿病定期検診 | 10 min | Chronic disease management, medication |
| mock_003 | acute_illness | 風邪症状の相談 | 5 min | Acute symptoms, prescriptions |
| mock_004 | medication_review | 多剤併用の確認 | 11 min | Polypharmacy, elderly care |
| mock_005 | specialist_referral | 専門医紹介 | 8 min | Referral process, emergency protocols |

## Data Structure

Each JSON file contains:

```json
{
  "id": "mock_XXX",
  "scenario": "scenario_type",
  "title": "日本語タイトル - English Title",
  "language": "ja",
  "duration_seconds": 420,
  "participants": {
    "doctor": { "name", "specialty", "hospital" },
    "patient": { "name", "age", "gender" }
  },
  "transcript": [
    {
      "speaker": "doctor|patient",
      "text": "対話テキスト",
      "timestamp_start": 0,
      "timestamp_end": 5
    }
  ],
  "expected_summary": {
    "chief_complaint": "主訴",
    "findings": ["所見1", "所見2"],
    "recommendations": ["推奨1", "推奨2"],
    "prescriptions": [...],
    "follow_up": "次回予定"
  }
}
```

## Usage

### For Testing AI Summarization

```python
import json

# Load mock recording
with open('scenario_01_general_checkup.json', 'r', encoding='utf-8') as f:
    mock = json.load(f)

# Extract transcript for AI processing
transcript_text = "\n".join([
    f"{t['speaker']}: {t['text']}"
    for t in mock['transcript']
])

# Send to AI service for summarization
# Compare output with mock['expected_summary']
```

### For Testing Audio Transcription

To generate actual audio files from these transcripts:

```bash
# Using gTTS or similar TTS engine
python scripts/generate_mock_audio.py --scenario mock_001
```

## Medical Terminology Coverage

These scenarios include:

- **Vital signs**: 血圧 (blood pressure), 体温 (temperature)
- **Lab values**: HbA1c, LDLコレステロール, 空腹時血糖値
- **Medications**: メトホルミン, アスピリン, オルメサルタン, etc.
- **Conditions**: 糖尿病, 狭心症, 扁桃炎, 骨粗鬆症
- **Procedures**: 心臓カテーテル検査, インフルエンザ検査
- **Dosage instructions**: 1日2回, 朝夕食後, 頓用 (as needed)

## Notes

- All patient names are fictional
- Medical values are realistic but not from real patients
- Transcripts use natural Japanese clinical dialogue patterns
- Expected summaries follow Japanese medical documentation standards

## Future Additions

Planned scenarios:
- Pediatric consultation (小児科)
- Mental health check-in (心療内科)
- Physical therapy follow-up (リハビリ)
- Emergency room visit (救急)
- Post-surgery follow-up (術後経過)
