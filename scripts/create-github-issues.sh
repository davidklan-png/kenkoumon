#!/usr/bin/env bash
#
# Kenkoumon — Create GitHub Milestones & Issues
#
# Prerequisites:
#   1. Install GitHub CLI: https://cli.github.com/
#   2. Authenticate: gh auth login
#   3. Run from the repo root: bash scripts/create-github-issues.sh
#
# Creates 6 labels, 8 milestones, and 46 issues.
# Labels are idempotent (skips existing). Milestones/issues will duplicate if run twice.

set -euo pipefail

REPO="davidklan-png/kenkoumon"

echo "=== Kenkoumon: Creating GitHub Milestones & Issues ==="
echo "Repository: $REPO"
echo ""

# ─────────────────────────────────────────────
# Labels
# ─────────────────────────────────────────────
echo "--- Creating labels ---"

gh label create "enhancement"    --repo "$REPO" --color "0e8a16" --description "New feature or capability" 2>/dev/null || echo "  Label 'enhancement' already exists"
gh label create "infrastructure" --repo "$REPO" --color "5319e7" --description "CI/CD, deployment, database, hosting, tooling" 2>/dev/null || echo "  Label 'infrastructure' already exists"
gh label create "documentation"  --repo "$REPO" --color "0075ca" --description "Documentation changes or additions" 2>/dev/null || echo "  Label 'documentation' already exists"
gh label create "research"       --repo "$REPO" --color "fbca04" --description "Investigation, evaluation, or validation work" 2>/dev/null || echo "  Label 'research' already exists"
gh label create "design"         --repo "$REPO" --color "e99695" --description "UI/UX design decisions or implementation" 2>/dev/null || echo "  Label 'design' already exists"
gh label create "testing"        --repo "$REPO" --color "d93f0b" --description "Test creation, integration testing, QA" 2>/dev/null || echo "  Label 'testing' already exists"

echo ""

# ─────────────────────────────────────────────
# Milestones
# ─────────────────────────────────────────────
echo "--- Creating milestones ---"

gh api repos/$REPO/milestones -f title="M1: Experiment Zero Tooling & Execution" -f state=open -f description="Build lightweight scripts to make the manual pipeline repeatable, then execute Experiment Zero.

Timeline: Weeks 1-4
Gate: accurate + useful = proceed; accurate + not useful = redesign; not accurate = investigate." 2>/dev/null && echo "  Created M1" || echo "  Milestone 'M1' already exists"

gh api repos/$REPO/milestones -f title="M2: Expanded Validation" -f state=open -f description="Scale from 1 user/1 doctor to 5 users and 3-5 doctors. Stage 1 from docs/VISION.md.

Timeline: Weeks 5-12
Gate: >70% doctors find useful AND >70% would pay ¥1,500/month = proceed to engineering." 2>/dev/null && echo "  Created M2" || echo "  Milestone 'M2' already exists"

gh api repos/$REPO/milestones -f title="M3: Repository Scaffolding" -f state=open -f description="Set up development environment, finalize tech stack, establish project structure. No feature code.

Timeline: Weeks 13-14" 2>/dev/null && echo "  Created M3" || echo "  Milestone 'M3' already exists"

gh api repos/$REPO/milestones -f title="M4: Core Pipeline — Record, Transcribe, Generate" -f state=open -f description="Features F1, F2, F3. The core value chain: record audio → transcribe Japanese → generate structured report.

Timeline: Weeks 15-19" 2>/dev/null && echo "  Created M4" || echo "  Milestone 'M4' already exists"

gh api repos/$REPO/milestones -f title="M5: Patient Review & Notes (F4)" -f state=open -f description="Patient-facing report viewing and ability to add notes (Section 4). Feature F4.

Timeline: Weeks 19-21" 2>/dev/null && echo "  Created M5" || echo "  Milestone 'M5' already exists"

gh api repos/$REPO/milestones -f title="M6: Secure Sharing & Auth (F5)" -f state=open -f description="Authentication and secure link sharing mechanism. Feature F5.

Timeline: Weeks 21-24" 2>/dev/null && echo "  Created M6" || echo "  Milestone 'M6' already exists"

gh api repos/$REPO/milestones -f title="M7: Session History & Encryption (F6)" -f state=open -f description="Session history (F6), encryption requirements, APPI data residency compliance.

Timeline: Weeks 24-26" 2>/dev/null && echo "  Created M7" || echo "  Milestone 'M7' already exists"

gh api repos/$REPO/milestones -f title="M8: Integration, Testing & Launch" -f state=open -f description="Integrate all features, test end-to-end, add analytics, launch to validation users.

Timeline: Weeks 26-28
Success: 50+ sessions, >95% accuracy, >60% share rate, >70% retention." 2>/dev/null && echo "  Created M8" || echo "  Milestone 'M8' already exists"

echo ""

# ─────────────────────────────────────────────
# Milestone titles (use full title with gh issue create -m)
# ─────────────────────────────────────────────
M1_TITLE="M1: Experiment Zero Tooling & Execution"
M2_TITLE="M2: Expanded Validation"
M3_TITLE="M3: Repository Scaffolding"
M4_TITLE="M4: Core Pipeline — Record, Transcribe, Generate"
M5_TITLE="M5: Patient Review & Notes (F4)"
M6_TITLE="M6: Secure Sharing & Auth (F5)"
M7_TITLE="M7: Session History & Encryption (F6)"
M8_TITLE="M8: Integration, Testing & Launch"

echo "Using milestone titles:"
echo "  M1: $M1_TITLE"
echo "  M2: $M2_TITLE"
echo "  M3: $M3_TITLE"
echo "  M4: $M4_TITLE"
echo "  M5: $M5_TITLE"
echo "  M6: $M6_TITLE"
echo "  M7: $M7_TITLE"
echo "  M8: $M8_TITLE"
echo ""

# ─────────────────────────────────────────────
# Milestone 1: Experiment Zero Tooling & Execution
# ─────────────────────────────────────────────
echo "--- Creating Milestone 1 issues (Experiment Zero) ---"

gh issue create --repo "$REPO" -m "$M1_TITLE" \
  --label "enhancement" --label "infrastructure" \
  --title "Create Whisper transcription script" \
  --body "## Description
Create a CLI script (Python) that takes a Japanese audio file (m4a, wav, mp3) and calls the OpenAI Whisper API with \`language=ja\` to produce a text transcript.

This is Step 2 of the manual pipeline in \`docs/EXPERIMENT-ZERO.md\`.

## Acceptance Criteria
- Running \`python transcribe.py recording.m4a\` produces \`recording.txt\` with Japanese text
- Supports m4a, wav, and mp3 input formats
- Includes instructions for getting an OpenAI API key
- API key configurable via environment variable

## References
- \`docs/EXPERIMENT-ZERO.md\` Step 2"

gh issue create --repo "$REPO" -m "$M1_TITLE" \
  --label "enhancement" --label "infrastructure" \
  --title "Create report generation script" \
  --body "## Description
Create a CLI script that takes a Japanese transcript text file, injects it into the processing prompt from \`docs/PROCESSING-PROMPT.md\`, sends it to Claude API (or GPT-4), and saves the structured report as a Markdown file.

Support selecting the LLM provider via a flag or environment variable.

## Acceptance Criteria
- Running \`python generate_report.py transcript.txt --provider claude\` produces a Markdown report
- Report contains all four sections defined in \`docs/DOCTOR-REPORT-SPEC.md\`
- Supports both Claude and GPT-4 providers
- API keys configurable via environment variables

## References
- \`docs/EXPERIMENT-ZERO.md\` Step 3
- \`docs/PROCESSING-PROMPT.md\`
- \`docs/DOCTOR-REPORT-SPEC.md\`"

gh issue create --repo "$REPO" -m "$M1_TITLE" \
  --label "documentation" \
  --title "Create self-evaluation scorecard template" \
  --body "## Description
Create a Markdown template (\`docs/SCORECARD-TEMPLATE.md\`) based on the self-evaluation questions in \`docs/EXPERIMENT-ZERO.md\` Step 4.

## Fields to Include
- Transcription accuracy rating (1-10)
- Per-section quality rating (1-10) for each of the 4 report sections
- Factual errors found (list)
- Japanese register assessment
- Willingness-to-pay response
- Free-text notes

## Acceptance Criteria
- Template covers all evaluation criteria from the experiment protocol
- Template covers quality criteria from \`docs/DOCTOR-REPORT-SPEC.md\`

## References
- \`docs/EXPERIMENT-ZERO.md\` Step 4
- \`docs/DOCTOR-REPORT-SPEC.md\`"

gh issue create --repo "$REPO" -m "$M1_TITLE" \
  --label "enhancement" \
  --title "Create end-to-end pipeline script" \
  --body "## Description
Create a wrapper script that chains transcription and report generation: audio file in, timestamped \`runs/YYYY-MM-DD/\` directory out (transcript + report + blank scorecard).

## Acceptance Criteria
- Running \`python pipeline.py recording.m4a\` produces a timestamped directory containing the transcript, report, and blank scorecard
- Handles errors gracefully (failed transcription, failed generation)

## Dependencies
- Transcription script
- Report generation script
- Scorecard template"

gh issue create --repo "$REPO" -m "$M1_TITLE" \
  --label "research" \
  --title "Execute Experiment Zero — first doctor visit" \
  --body "## Description
Execute the full Experiment Zero protocol from \`docs/EXPERIMENT-ZERO.md\`:

1. Attend a doctor appointment
2. Ask permission to record (「すみません、自分の記録のために会話を録音してもよろしいでしょうか？」)
3. Record the consultation
4. Run the pipeline
5. Self-evaluate using the scorecard
6. Document results

This is the critical validation gate for the entire project.

## Acceptance Criteria
- Completed scorecard with all fields filled
- Decision gate assessment documented
- Results saved in \`runs/\` directory

## Dependencies
- End-to-end pipeline script

## References
- \`docs/EXPERIMENT-ZERO.md\`"

gh issue create --repo "$REPO" -m "$M1_TITLE" \
  --label "research" \
  --title "Share report with doctor and record feedback" \
  --body "## Description
At the next doctor visit, present the generated report (printed or emailed). Use the Japanese script:

「前回の診察の内容をAIでまとめたものです。次回の参考になればと思いまして。」

## Feedback to Collect
- Was it accurate?
- Was it useful?
- Would they want to receive it regularly?
- What would they change?

## Acceptance Criteria
- Doctor feedback documented alongside the scorecard
- Go/no-go decision for expanded validation recorded

## Dependencies
- Experiment Zero execution

## References
- \`docs/EXPERIMENT-ZERO.md\` Steps 6-7"

gh issue create --repo "$REPO" -m "$M1_TITLE" \
  --label "documentation" \
  --title "Document Experiment Zero results and prompt tuning" \
  --body "## Description
After completing the first experiment run:

1. Update \`docs/PROCESSING-PROMPT.md\` with prompt tuning notes
2. Document transcription issues and medical terms the AI got wrong
3. Assess Section 3 (Next Visit Prep) quality
4. Document Japanese register feedback from doctor
5. Reassess RISK-2 and RISK-3 per \`docs/RISK-REGISTER.md\` review schedule

## Acceptance Criteria
- Prompt tuning notes filled in
- Risk register updated with Experiment Zero findings
- Clear recommendation for whether to proceed, redesign, or investigate

## Dependencies
- Experiment execution and doctor feedback

## References
- \`docs/PROCESSING-PROMPT.md\`
- \`docs/RISK-REGISTER.md\`"

echo "  Created 7 issues for M1"

# ─────────────────────────────────────────────
# Milestone 2: Expanded Validation
# ─────────────────────────────────────────────
echo "--- Creating Milestone 2 issues (Expanded Validation) ---"

gh issue create --repo "$REPO" -m "$M2_TITLE" \
  --label "research" \
  --title "Recruit 5 expat testers" \
  --body "## Description
Identify and recruit 5 English-speaking expats in Japan who have upcoming doctor appointments. Target a mix of visit types (general checkup, specialist, follow-up).

Provide each tester with the recording script, pipeline tools, and scorecard template.

## Acceptance Criteria
- 5 testers recruited with scheduled or recent doctor visits
- Mix of visit types represented
- Tracking spreadsheet or Markdown tracker set up

## Dependencies
- Milestone 1 complete"

gh issue create --repo "$REPO" -m "$M2_TITLE" \
  --label "research" \
  --title "Run pipeline across 10+ sessions" \
  --body "## Description
Process recordings from the 5 testers (target: 2+ sessions each, 10+ total). Collect scorecards and track accuracy patterns across different doctors, clinics, and audio conditions.

## Track
- Transcription accuracy per session
- Failure modes (background noise, mumbling, dialect, cross-talk)
- Accuracy trends

## Acceptance Criteria
- 10+ sessions processed
- Scorecards collected for all sessions
- Accuracy trends documented

## Dependencies
- Testers recruited"

gh issue create --repo "$REPO" -m "$M2_TITLE" \
  --label "research" \
  --title "Collect doctor feedback from 3+ doctors" \
  --body "## Description
At least 3 different doctors should see and comment on AI-generated reports.

## Track
- Usefulness rating
- Accuracy rating
- What they would change
- Whether they want to receive these regularly

## Acceptance Criteria
- Feedback from 3+ doctors documented
- >70% find it useful (per Stage 1 success criteria in \`docs/VISION.md\`)

## Dependencies
- Sessions processed"

gh issue create --repo "$REPO" -m "$M2_TITLE" \
  --label "research" \
  --title "Evaluate transcription alternatives" \
  --body "## Description
If Whisper accuracy is below 90% on medical terms (RISK-2 threshold), evaluate alternatives:
- ReazonSpeech (Japanese-specialized)
- Azure Speech Services (Japan East)
- Google Cloud Speech-to-Text

Run the same audio files through multiple services and compare accuracy on medical terminology.

## Acceptance Criteria
- Comparison table of transcription services with medical term accuracy percentages
- Recommendation for MVP transcription provider

## Dependencies
- Accuracy data from pipeline runs

## References
- \`docs/RISK-REGISTER.md\` RISK-2"

gh issue create --repo "$REPO" -m "$M2_TITLE" \
  --label "research" \
  --title "Evaluate LLM providers for report generation" \
  --body "## Description
Run the same transcripts through both providers:
- Claude (via AWS Bedrock Tokyo region)
- GPT-4 (via Azure Japan East)

## Evaluate
- Section 3 observation quality
- Medical Japanese register appropriateness
- Entity extraction accuracy
- Japan-region availability for APPI compliance

## Acceptance Criteria
- Side-by-side comparison documented
- Recommended LLM provider selected with rationale

## References
- \`docs/DECISIONS-LOG.md\` Decision 3"

gh issue create --repo "$REPO" -m "$M2_TITLE" \
  --label "research" --label "documentation" \
  --title "Initial APPI legal consultation" \
  --body "## Description
Get a preliminary legal opinion on APPI compliance (budget: ¥200-500K).

## Key Questions
1. Is recording medical conversations with patient consent legally permissible?
2. What consent documentation is needed?
3. Does the planned Japan-region cloud architecture satisfy APPI data residency?
4. What are the requirements for handling medical audio data?
5. Are there restrictions on sharing AI-generated medical reports via secure links?

## Acceptance Criteria
- Written legal opinion received
- APPI compliance requirements documented
- Any required architectural changes identified

## References
- \`docs/RISK-REGISTER.md\` RISK-5
- \`docs/ARCHITECTURE.md\` Data Residency section"

gh issue create --repo "$REPO" -m "$M2_TITLE" \
  --label "documentation" \
  --title "Validation phase decision gate" \
  --body "## Description
Compile all validation results into a go/no-go decision document.

## Check Against Stage 1 Success Criteria
- [ ] >70% of doctors find reports useful
- [ ] >70% of test users would pay ¥1,500/month
- [ ] >85% medical term accuracy (RISK-2 kill criteria)
- [ ] Doctor refusal rate acceptable (RISK-1 signals)

## Outcomes
- **Go:** Proceed to MVP engineering (Milestone 3)
- **Conditional go:** Proceed with specific changes
- **No-go:** Document what needs to change

## Acceptance Criteria
- Decision document written with explicit go/no-go reasoning

## Dependencies
- All validation issues complete"

echo "  Created 7 issues for M2"

# ─────────────────────────────────────────────
# Milestone 3: Repository Scaffolding
# ─────────────────────────────────────────────
echo "--- Creating Milestone 3 issues (Repo Scaffolding) ---"

gh issue create --repo "$REPO" -m "$M3_TITLE" \
  --label "research" --label "documentation" \
  --title "Finalize mobile framework decision (React Native vs Flutter)" \
  --body "## Description
Make the final decision on mobile framework per \`docs/MVP-SPEC.md\`.

## Evaluate Against
- Audio recording API quality on iOS and Android
- Japan-region cloud SDK support
- Solo-developer productivity
- Community support for Japanese language handling
- Founder's existing expertise

## Acceptance Criteria
- Decision documented with rationale
- \`docs/DECISIONS-LOG.md\` updated

## References
- \`docs/MVP-SPEC.md\` Technical Stack
- \`docs/DECISIONS-LOG.md\`"

gh issue create --repo "$REPO" -m "$M3_TITLE" \
  --label "infrastructure" \
  --title "Initialize mobile app project" \
  --body "## Description
Initialize the mobile project using the chosen framework.

## Setup
- Directory structure: screens, components, services, models, utils, tests
- TypeScript config (React Native) or analysis options (Flutter)
- Framework-appropriate \`.gitignore\`
- Development setup instructions

## Acceptance Criteria
- App builds and runs on iOS simulator and Android emulator
- Shows a placeholder screen
- Project structure follows framework conventions

## Dependencies
- Framework decision"

gh issue create --repo "$REPO" -m "$M3_TITLE" \
  --label "infrastructure" \
  --title "Set up backend API project" \
  --body "## Description
Initialize the backend API project (Node.js/Express or Python/FastAPI).

## Setup
- Directory structure: routes, controllers, models, services, middleware, tests
- \`.env.example\` with placeholders for all required env vars
- \`Dockerfile\` for containerized development
- Health check endpoint (\`GET /health\`)

## Acceptance Criteria
- Server starts and responds to \`GET /health\`
- Docker build works
- \`.env.example\` documents all required environment variables"

gh issue create --repo "$REPO" -m "$M3_TITLE" \
  --label "infrastructure" \
  --title "Set up PostgreSQL with initial schema" \
  --body "## Description
Create the initial database schema based on \`docs/MVP-SPEC.md\` entity data model.

## Tables
- \`patients\` — account info
- \`sessions\` — date, audio_reference, transcript_ja, report_ja, patient_notes, status
- \`providers\` — name_ja, name_en, specialty, source_session_id
- \`medications\` — name_ja, name_en, dosage, status, source_session_id
- \`conditions\` — name_ja, name_en, status, source_session_id
- \`instructions\` — content_ja, category, due_date, source_session_id
- \`share_links\` — token, session_id, expires_at, created_at, revoked

All entity tables include: source_session_id, confidence, patient_confirmed.

## Requirements
- Database migrations (Prisma, Knex, Alembic, etc.)
- UTF-8 for Japanese text
- \`docker-compose.yml\` for local PostgreSQL

## Acceptance Criteria
- Migrations run successfully
- Schema matches entity data model
- \`docker-compose up\` starts PostgreSQL with schema applied

## Dependencies
- Backend project

## References
- \`docs/MVP-SPEC.md\` Entity Data Model
- \`docs/ARCHITECTURE.md\`"

gh issue create --repo "$REPO" -m "$M3_TITLE" \
  --label "infrastructure" \
  --title "Set up CI pipeline" \
  --body "## Description
Configure GitHub Actions for linting, type checking, unit tests, and build verification.

## Triggers
- Push to main
- Pull requests

## Acceptance Criteria
- CI runs on push
- Green check on initial codebase
- Single workflow file per project

## Dependencies
- Mobile and backend projects exist"

gh issue create --repo "$REPO" -m "$M3_TITLE" \
  --label "enhancement" --label "infrastructure" \
  --title "Create AI service abstraction layer" \
  --body "## Description
Per Decision 3 in \`docs/DECISIONS-LOG.md\`, the AI layer must be abstracted behind an interface for provider swapping.

## Interfaces
- \`TranscriptionService\` — input: audio file → output: Japanese text
- \`ReportGenerationService\` — input: transcript → output: structured report + extracted entities

## Implementations
- Adapter for chosen transcription provider
- Adapter for chosen LLM provider
- Provider selection via environment variable

## Acceptance Criteria
- Interfaces defined with clear contracts
- At least one concrete implementation for each
- Provider swappable via config without code changes

## Dependencies
- Backend project
- Provider decisions from validation phase

## References
- \`docs/DECISIONS-LOG.md\` Decision 3
- \`docs/ARCHITECTURE.md\`"

echo "  Created 6 issues for M3"

# ─────────────────────────────────────────────
# Milestone 4: Core Pipeline
# ─────────────────────────────────────────────
echo "--- Creating Milestone 4 issues (Core Pipeline) ---"

gh issue create --repo "$REPO" -m "$M4_TITLE" \
  --label "enhancement" \
  --title "Implement in-app audio recording (F1)" \
  --body "## Description
Build the audio recording screen. Requirements from \`docs/MVP-SPEC.md\` F1:
- Record audio within the app
- Patient controls start/stop
- On-device storage until upload
- AAC/m4a format

## UI
- Large record button, timer, stop button

## Not Included
Background recording, silence detection, noise cancellation, multi-device.

## Acceptance Criteria
- User can record, see timer, stop
- Audio file saved locally
- Audio quality sufficient for transcription

## Dependencies
- Mobile project scaffolded

## References
- \`docs/MVP-SPEC.md\` F1"

gh issue create --repo "$REPO" -m "$M4_TITLE" \
  --label "enhancement" \
  --title "Implement audio upload to backend" \
  --body "## Description
After recording, upload audio to backend. Create session record with status flow: uploading → uploaded.

## Requirements
- Encrypted storage (AES-256)
- Upload progress indication
- Network failure handling (retry/resume)

## Acceptance Criteria
- Audio uploaded from app to backend
- Session record created in database
- Upload progress shown
- Encrypted at rest

## Dependencies
- Audio recording, database schema"

gh issue create --repo "$REPO" -m "$M4_TITLE" \
  --label "enhancement" \
  --title "Implement transcription pipeline (F2)" \
  --body "## Description
Backend sends uploaded audio to transcription service via abstraction layer.

## Requirements (\`docs/MVP-SPEC.md\` F2)
- Japanese audio → Japanese text
- Medical terminology accuracy critical
- API-based, minutes acceptable

## Status Flow
uploaded → transcribing → transcribed (or transcription_failed)

## Acceptance Criteria
- Audio transcribed via configured provider
- Japanese transcript stored in database
- Session status updated correctly
- Errors handled gracefully

## Dependencies
- AI abstraction layer, audio upload

## References
- \`docs/MVP-SPEC.md\` F2"

gh issue create --repo "$REPO" -m "$M4_TITLE" \
  --label "enhancement" \
  --title "Implement report generation pipeline (F3)" \
  --body "## Description
Send transcript + processing prompt to LLM. Parse 4-section report per \`docs/DOCTOR-REPORT-SPEC.md\`. Extract entities to DB tables.

## Status Flow
transcribed → generating → complete

## Entity Extraction
- Medications, conditions, instructions, providers, tests
- Store with source_session_id linkage
- Bilingual labels (JP + EN) where available

## Acceptance Criteria
- Report generated with all four sections
- Entities extracted and stored
- Session status reflects completion

## Dependencies
- AI abstraction layer, transcription pipeline

## References
- \`docs/MVP-SPEC.md\` F3
- \`docs/PROCESSING-PROMPT.md\`
- \`docs/DOCTOR-REPORT-SPEC.md\`"

gh issue create --repo "$REPO" -m "$M4_TITLE" \
  --label "enhancement" \
  --title "Implement processing status polling" \
  --body "## Description
App polls session status every 10-15s. Shows: uploading → transcribing → generating → complete.

## Acceptance Criteria
- App shows real-time processing status
- User informed when report is ready
- Works when app is in foreground

## Dependencies
- Pipeline stages exist"

gh issue create --repo "$REPO" -m "$M4_TITLE" \
  --label "infrastructure" \
  --title "Add processing time monitoring" \
  --body "## Description
Log processing times per stage (upload, transcription, generation). NFR target: <5 minutes total.

## Acceptance Criteria
- Processing times logged per session per stage
- Can query average and p95 processing times

## Dependencies
- Pipeline stages exist

## References
- \`docs/MVP-SPEC.md\` Non-Functional Requirements"

echo "  Created 6 issues for M4"

# ─────────────────────────────────────────────
# Milestone 5: Patient Review & Notes
# ─────────────────────────────────────────────
echo "--- Creating Milestone 5 issues (Patient Review) ---"

gh issue create --repo "$REPO" -m "$M5_TITLE" \
  --label "enhancement" --label "design" \
  --title "Build report viewing screen" \
  --body "## Description
Render all 4 report sections in Japanese with proper medical typography.

## Sections
1. 診察内容の要約 (Visit Summary)
2. 主な医療情報 (Key Medical Information)
3. 次回診察に向けて (For Next Visit)
4. 患者からのメモ (Patient Notes) — visually distinct as editable

Include header (date, patient, doctor) and disclaimer footer. Scannable in 2-3 minutes.

## Acceptance Criteria
- All four sections render correctly
- Japanese text displays properly
- Section 4 visually distinct from read-only sections

## Dependencies
- Reports exist to display

## References
- \`docs/DOCTOR-REPORT-SPEC.md\`"

gh issue create --repo "$REPO" -m "$M5_TITLE" \
  --label "enhancement" \
  --title "Implement patient notes editing (Section 4)" \
  --body "## Description
Per \`docs/MVP-SPEC.md\` F4: patient can add notes in Section 4 (患者からのメモ).

## Requirements
- Free-text input in Section 4
- Auto-save to patient_notes field
- Sections 1-3 read-only

## Acceptance Criteria
- Patient can add and edit notes
- Notes persist across app restarts
- Sections 1-3 cannot be edited

## Dependencies
- Report viewing screen"

gh issue create --repo "$REPO" -m "$M5_TITLE" \
  --label "enhancement" --label "design" \
  --title "Implement share now vs review later flow" \
  --body "## Description
Per Decision 4: patient chooses when to release. Two paths after processing:

1. **Share immediately** — generates secure link right away
2. **Review first** — view report, add notes, then share

Minimum viable workflow: stop recording → tap process and share → done.

## Acceptance Criteria
- Both paths work
- Immediate share creates link without review
- Review path allows notes then share

## Dependencies
- Report view and notes editing

## References
- \`docs/DECISIONS-LOG.md\` Decision 4
- \`docs/RISK-REGISTER.md\` RISK-7"

gh issue create --repo "$REPO" -m "$M5_TITLE" \
  --label "enhancement" --label "design" \
  --title "Build extracted entities display" \
  --body "## Description
Display extracted entities (medications, conditions, instructions, providers) in structured format within report view. Show bilingual labels (JP + EN).

## Acceptance Criteria
- Entities displayed in structured format in Section 2
- Bilingual labels shown
- Medications include dosage where extracted

## Dependencies
- Entity extraction, report screen

## References
- \`docs/ARCHITECTURE.md\` bilingual principle"

echo "  Created 4 issues for M5"

# ─────────────────────────────────────────────
# Milestone 6: Secure Sharing & Auth
# ─────────────────────────────────────────────
echo "--- Creating Milestone 6 issues (Secure Sharing & Auth) ---"

gh issue create --repo "$REPO" -m "$M6_TITLE" \
  --label "infrastructure" --label "enhancement" \
  --title "Implement patient authentication" \
  --body "## Description
Email/password auth with JWT sessions.

## Requirements
- Account creation with email verification
- Login and session management
- Password reset
- Per-patient encryption key generated on account creation
- Patients can only access their own data

## Acceptance Criteria
- Create account, log in, access only own data
- Per-patient encryption key generated
- Password reset works

## Dependencies
- Database schema

## References
- \`docs/MVP-SPEC.md\` Technical Stack
- \`docs/ARCHITECTURE.md\` Security"

gh issue create --repo "$REPO" -m "$M6_TITLE" \
  --label "enhancement" \
  --title "Implement secure link generation (F5)" \
  --body "## Description
Per \`docs/MVP-SPEC.md\` F5: generate unique, expiring secure link.

## Requirements
- Cryptographically random token
- Store in share_links table with expiration (default 30 days)
- No auth needed to view the link

## Acceptance Criteria
- Unique URL generated per share action
- Token is cryptographically secure
- Expiration stored and configurable

## Dependencies
- Database and auth

## References
- \`docs/MVP-SPEC.md\` F5"

gh issue create --repo "$REPO" -m "$M6_TITLE" \
  --label "enhancement" --label "design" \
  --title "Build public report viewing page (web)" \
  --body "## Description
Web page at share link URL — this is what the doctor sees.

## Requirements
- Professional, clean design
- All 4 sections in Japanese
- Responsive (desktop and mobile)
- No login required
- Disclaimer footer

## Acceptance Criteria
- Valid link shows full report
- Responsive on all devices
- Expired links show expiration message
- Invalid tokens show 404

## Dependencies
- Secure link generation

## References
- \`docs/DECISIONS-LOG.md\` Decision 6"

gh issue create --repo "$REPO" -m "$M6_TITLE" \
  --label "enhancement" --label "infrastructure" \
  --title "Implement link expiration and revocation" \
  --body "## Description
Enforce link expiration and provide link management.

## Requirements
- Check expires_at on access
- Patient can revoke links
- Patient can view active links per session
- Configurable duration: 7, 14, 30 (default), 90 days

## Acceptance Criteria
- Expired links blocked
- Patient can revoke and view active links

## Dependencies
- Secure links and public page"

gh issue create --repo "$REPO" -m "$M6_TITLE" \
  --label "enhancement" \
  --title "Implement share delivery options" \
  --body "## Description
Per F5: patient shares via any channel.

## Methods
1. Copy link to clipboard
2. System share sheet (LINE, email, etc.)
3. QR code generation

## Acceptance Criteria
- All three methods work
- QR code encodes full URL and is scannable

## Dependencies
- Secure link generation"

echo "  Created 5 issues for M6"

# ─────────────────────────────────────────────
# Milestone 7: Session History & Encryption
# ─────────────────────────────────────────────
echo "--- Creating Milestone 7 issues (Session History & Encryption) ---"

gh issue create --repo "$REPO" -m "$M7_TITLE" \
  --label "enhancement" --label "design" \
  --title "Build session history screen (F6)" \
  --body "## Description
Per \`docs/MVP-SPEC.md\` F6: chronological list of sessions.

## Display Per Session
- Date, provider name (or Unknown), processing status
- Sorted newest first
- Tap to view report

## Not Included
Search, filtering, longitudinal analysis, data export.

## Acceptance Criteria
- Patient sees all their sessions with accurate status
- Tapping navigates to report
- Smooth scrolling

## Dependencies
- Auth and report view"

gh issue create --repo "$REPO" -m "$M7_TITLE" \
  --label "infrastructure" --label "enhancement" \
  --title "Implement AES-256 encryption at rest" \
  --body "## Description
Per \`docs/ARCHITECTURE.md\`: AES-256 at rest for audio, transcripts, and reports.

## Requirements
- Per-patient encryption keys
- Key management via KMS or application-level KEK
- Patient can delete audio files
- Transparent decryption for authorized access

## Acceptance Criteria
- Data encrypted at rest with per-patient keys
- Patient audio deletion works
- Decryption transparent for authorized access

## Dependencies
- Per-patient keys from auth

## References
- \`docs/ARCHITECTURE.md\` Security
- \`docs/MVP-SPEC.md\` NFRs"

gh issue create --repo "$REPO" -m "$M7_TITLE" \
  --label "infrastructure" \
  --title "Configure TLS 1.3 transport security" \
  --body "## Description
Per \`docs/ARCHITECTURE.md\`: TLS 1.3 in transit.

## Requirements
- Backend enforces TLS 1.3
- SSL certificates (Let's Encrypt or ACM)
- Mobile app rejects insecure connections
- HTTP redirects to HTTPS

## Acceptance Criteria
- All connections use TLS 1.3
- HTTP redirected to HTTPS
- Mobile app rejects non-TLS

## Dependencies
- Backend exists"

gh issue create --repo "$REPO" -m "$M7_TITLE" \
  --label "infrastructure" \
  --title "Configure Japan-region deployment" \
  --body "## Description
Per APPI compliance: all data must reside in Japan region.

## Options (choose one)
- AWS Tokyo (ap-northeast-1)
- Azure Japan East
- GCP asia-northeast1

## Infrastructure
- Backend API, PostgreSQL, file storage, web server for share links

## Acceptance Criteria
- All infrastructure in Japan region
- No data transits outside Japan
- Deployment documented and reproducible
- Incorporates APPI requirements from legal consultation

## References
- \`docs/ARCHITECTURE.md\` Data Residency
- \`docs/MVP-SPEC.md\` NFRs"

gh issue create --repo "$REPO" -m "$M7_TITLE" \
  --label "enhancement" \
  --title "Implement patient-controlled audio deletion" \
  --body "## Description
Per \`docs/ARCHITECTURE.md\`: patient-controlled audio deletion.

## Requirements
- Delete audio after report generation (transcript and report remain)
- Delete button on session detail screen
- Optional auto-delete after successful report generation

## Acceptance Criteria
- Patient can delete audio for any session
- Deletion is permanent
- Transcript and report remain accessible
- Auto-delete setting works

## Dependencies
- Session history and encryption in place"

echo "  Created 5 issues for M7"

# ─────────────────────────────────────────────
# Milestone 8: Integration & Launch
# ─────────────────────────────────────────────
echo "--- Creating Milestone 8 issues (Integration & Launch) ---"

gh issue create --repo "$REPO" -m "$M8_TITLE" \
  --label "testing" \
  --title "End-to-end integration testing" \
  --body "## Description
Test the complete flow: Record → Process → Review → Share → Doctor views.

## Test
- Both 'share immediately' and 'review first' paths
- Real Japanese medical audio
- Both iOS and Android
- Processing within 5 minutes (NFR)

## Acceptance Criteria
- Complete flow works end-to-end on both platforms
- No blocking bugs
- Processing within 5 min target
- UX friction points documented

## Dependencies
- Milestones 4-7 complete"

gh issue create --repo "$REPO" -m "$M8_TITLE" \
  --label "documentation" --label "design" \
  --title "Add disclaimers and legal text" \
  --body "## Description
Add required disclaimers throughout app and shared reports.

## Required
1. Report disclaimer: AI-generated, not a medical record
2. Terms of service: wellness tool, not medical device
3. Privacy policy: data handling, APPI, encryption
4. Recording consent guidance in-app

## Acceptance Criteria
- All disclaimers present
- Wellness tool positioning clear throughout

## Dependencies
- Report views exist

## References
- \`docs/DOCTOR-REPORT-SPEC.md\` footer
- \`docs/RISK-REGISTER.md\` RISK-3"

gh issue create --repo "$REPO" -m "$M8_TITLE" \
  --label "infrastructure" \
  --title "Implement validation metrics tracking" \
  --body "## Description
Track MVP validation metrics from \`docs/MVP-SPEC.md\`.

## Server-Side
- Sessions created/completed, share rate, link access

## In-App Survey
- Report accuracy rating, doctor feedback, willingness-to-pay

## Targets
- 50+ sessions, >95% accuracy, >60% share rate
- >70% retention, >50% doctor approval, >60% WTP

## Acceptance Criteria
- All trackable metrics recorded
- Survey triggerable in-app
- Metrics queryable

## Dependencies
- Pipeline and sharing exist"

gh issue create --repo "$REPO" -m "$M8_TITLE" \
  --label "testing" --label "enhancement" \
  --title "Error handling and edge case hardening" \
  --body "## Description
Handle: upload failures, API timeouts, poor audio quality, network loss, stuck sessions, no extractable entities, very long recordings (>30 min).

## Acceptance Criteria
- All error scenarios handled gracefully
- No sessions stuck in unrecoverable states
- Clear error messages for each failure type

## Dependencies
- Pipeline exists"

gh issue create --repo "$REPO" -m "$M8_TITLE" \
  --label "infrastructure" \
  --title "Prepare TestFlight/internal testing build" \
  --body "## Description
Prepare app for distribution to 10-20 validation users.

## Distribution
- iOS: TestFlight
- Android: Internal testing track or direct APK

## Onboarding
- What the app does
- How to record
- Consent script in Japanese

## Acceptance Criteria
- App installable on both platforms
- Onboarding flow explains product
- Backend deployed to Japan region

## Dependencies
- Integration testing passes"

gh issue create --repo "$REPO" -m "$M8_TITLE" \
  --label "research" \
  --title "Launch to validation users and begin metric collection" \
  --body "## Description
Distribute app to 10+ users. Target 50+ sessions over 4-8 weeks.

## Goals
- Establish feedback loop
- Collect meaningful retention data
- Validate MVP metrics

## Acceptance Criteria
- App distributed to 10+ users
- Sessions being recorded
- Metrics being collected
- Feedback loop established

## Dependencies
- Analytics and distribution ready

## References
- \`docs/MVP-SPEC.md\` Validation Metrics"

echo "  Created 6 issues for M8"

echo ""
echo "=== Done! ==="
echo "Created: 6 labels, 8 milestones, 46 issues"
echo ""
echo "View milestones: gh milestone list --repo $REPO"
echo "View issues:     gh issue list --repo $REPO --state open --limit 50"
