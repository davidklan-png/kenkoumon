# 健康門 Kenkoumon — Patient-Owned Medical Visit Intelligence

> *Your health conversations. Your data. Your control.*

Kenkoumon records doctor-patient consultations and uses AI to produce structured, bilingual medical reports — giving patients a complete understanding of their visits and giving doctors a prepared briefing before the next appointment.

## The Problem

Every year, millions of patients walk out of doctor's offices having forgotten half of what was said. For expats and foreign residents navigating healthcare in a second language, the problem is exponentially worse. Critical instructions get lost, follow-up items are forgotten, and doctors have no insight into what the patient actually understood.

## The Solution

A patient-owned tool that:

1. **Records** the doctor-patient consultation (with consent)
2. **Processes** the audio into a structured medical report in the doctor's language
3. **Shares** a prepared briefing with the doctor via secure link before the next visit
4. **Accumulates** into a longitudinal health profile the patient fully controls

## Current Phase: Experiment Zero

Before building any product, we validate the core hypothesis with a zero-infrastructure experiment. See [EXPERIMENT-ZERO.md](docs/EXPERIMENT-ZERO.md) for the complete protocol.

**Hypothesis:** AI can turn a recorded Japanese medical consultation into a structured Japanese-language doctor briefing that physicians find genuinely useful.

## Core Principles

- **Patient owns everything.** All data, all decisions about sharing, all exports.
- **Doctor receives, never logs in.** The doctor gets a secure link to a report. No portal, no app, no vendor relationship.
- **AI extracts, patient controls.** The AI structures information from conversations. The patient decides what gets shared and with whom.
- **Open data, your AI.** Health data exports in open formats. Use any AI you trust to query your own health data.
- **Wellness tool, not medical device.** Assists communication and understanding. Does not provide clinical decision support.

## Project Documentation

| Document | Description |
|---|---|
| [EXPERIMENT-ZERO.md](docs/EXPERIMENT-ZERO.md) | The validation experiment protocol |
| [VISION.md](docs/VISION.md) | 90-day, 12-month, and 5-year product roadmap |
| [BUSINESS-MODEL.md](docs/BUSINESS-MODEL.md) | Pricing, revenue model, and growth strategy |
| [MVP-SPEC.md](docs/MVP-SPEC.md) | Post-validation MVP specification (F1–F6) |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Technical architecture and system design |
| [DECISIONS-LOG.md](docs/DECISIONS-LOG.md) | Numbered architectural and product decisions |
| [DOCTOR-REPORT-SPEC.md](docs/DOCTOR-REPORT-SPEC.md) | Report structure, quality criteria, and design principles |
| [REPORT-TEMPLATE.md](docs/REPORT-TEMPLATE.md) | LLM generation prompt for doctor briefing reports |
| [PROCESSING-PROMPT.md](docs/PROCESSING-PROMPT.md) | Processing prompt with tuning notes |
| [RISK-REGISTER.md](docs/RISK-REGISTER.md) | Active risks, mitigations, and kill criteria |

## Target Market (Initial)

English-speaking expats and foreign residents in Japan (~3 million people) who see Japanese-speaking doctors. The language and cultural communication gap makes the value proposition immediately obvious.

## Long-Term Vision

A patient-owned health data platform. Every medical interaction, every health checkup (健康診断), every blood test, every wearable reading — structured, bilingual, portable, and queryable by any AI the patient trusts. See [VISION.md](docs/VISION.md).

## Status

🔴 **Pre-validation** — Experiment Zero not yet run

## License

TBD
