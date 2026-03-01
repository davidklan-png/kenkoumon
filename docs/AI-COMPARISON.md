# Kenkoumon — AI Source Comparison

This document tracks the performance, accuracy, and cost of different AI sources for transcription and report generation.

## Purpose

Experiment Zero and subsequent validation will test multiple AI sources:
- **On-device:** whisper.cpp (CoreML/MLC), Llama.cpp, Gemma
- **User-hosted:** Ollama (Whisper, Llama, Mistral, etc.)
- **Cloud (optional fallback):** OpenAI Whisper, Claude, GPT-4

This comparison matrix will inform the default AI source selection and help users understand trade-offs.

## Comparison Matrix

### Transcription Sources

| Source | Medical Accuracy | Overall Accuracy | Speed | Cost | Device Requirements | Notes |
|--------|-----------------|------------------|-------|------|-------------------|-------|
| **whisper.cpp (on-device)** | TBD | TBD | TBD | Free | iPhone 14+/flagship Android | |
| **Ollama Whisper (user-hosted)** | TBD | TBD | TBD | Free (hardware) | Home server/NAS | |
| **OpenAI Whisper API** | TBD | TBD | TBD | ~$0.006/min | Any | Japan-region for APPI |

### Report Generation Sources

| Source | Medical Accuracy | Japanese Quality | Speed | Cost | Device Requirements | Notes |
|--------|-----------------|------------------|-------|------|-------------------|-------|
| **Llama.cpp 3.1/3.2** | TBD | TBD | TBD | Free | iPhone 14+/flagship Android | Multilingual |
| **Gemma 2/3** | TBD | TBD | TBD | Free | iPhone 14+/flagship Android | Google-backed |
| **Mistral (Ollama)** | TBD | TBD | TBD | Free (hardware) | Home server/NAS | |
| **Claude API** | TBD | TBD | TBD | ~$0.003/1K tokens | Any | Via AWS Bedrock Tokyo |
| **GPT-4 API** | TBD | TBD | TBD | ~$0.01/1K tokens | Any | Via Azure Japan East |

## Evaluation Criteria

### Transcription

| Metric | Target | Measurement |
|--------|--------|-------------|
| Medical term accuracy | >85% | Manual review of extracted medications, conditions |
| Overall word accuracy | >90% | Word error rate against manual transcript |
| Processing speed | <2 min / 10 min audio | End-to-end processing time |
| Battery impact | <20% per session | Battery drain on target device |

### Report Generation

| Metric | Target | Measurement |
|--------|--------|-------------|
| Medical accuracy | No critical errors | Manual review for medication/dosage errors |
| Section quality | Doctor-rated useful | Doctor feedback survey |
| Japanese register | Appropriate politeness | Doctor feedback |
| Processing speed | <3 min / transcript | End-to-end generation time |
| Battery impact | <30% per session | Battery drain on target device |

## Test Results Template

```
Session ID: YYYY-MM-DD-doctor
Device: iPhone 15 Pro / Galaxy S24 / etc.
Audio duration: X minutes

TRANSCRIPTION
Source: [on-device/Ollama/Cloud]
Medical accuracy: X/10
Overall accuracy: X/10
Processing time: X seconds

REPORT GENERATION
Source: [Llama/Gemma/Mistral/Claude/GPT-4]
Medical accuracy: X/10
Japanese quality: X/10
Processing time: X seconds

DOCTOR FEEDBACK
Usefulness: X/10
Accuracy: X/10
Would want to receive: [Yes/No]
Comments: [...]
```

## Decision Framework

### Default AI Source Selection

After validation, the default will be selected based on:

1. **Accuracy:** Must meet >85% medical term accuracy threshold
2. **Performance:** Must complete in <5 minutes total on target device
3. **Cost:** Prefer free/local options when quality is comparable
4. **Privacy:** Prefer on-device > user-hosted > cloud

### User Choice Matrix

| User Situation | Recommended Source |
|---------------|-------------------|
| iPhone 14+ / flagship Android | On-device (default) |
| Older phone but home server | User-hosted Ollama |
| Older phone, no server | Cloud fallback (optional) |
| Maximum privacy priority | On-device or user-hosted only |
| Maximum accuracy priority | Best performing source (may be cloud) |

## Notes from Experiment Zero

*To be filled during M1 execution...*

- [ ] First test session date
- [ ] Initial observations on accuracy
- [ ] Device performance notes
- [ ] Doctor feedback summary

## References

- [docs/EXPERIMENT-ZERO.md](EXPERIMENT-ZERO.md) - Experiment protocol
- [docs/ARCHITECTURE.md](ARCHITECTURE.md) - AI abstraction layer design
- [docs/MVP-SPEC.md](MVP-SPEC.md) - Technical stack
- [docs/DECISIONS-LOG.md](DECISIONS-LOG.md) - Decision 3: User-Controlled AI
