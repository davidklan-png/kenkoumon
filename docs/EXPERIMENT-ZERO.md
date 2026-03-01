# Experiment Zero — Validation Protocol

## Objective
Validate: Can AI turn a recorded Japanese medical consultation into a structured report that a Japanese doctor would find useful?

## Protocol

### Step 1: Record (During Appointment)
- Ask permission: 「すみません、自分の記録のために会話を録音してもよろしいでしょうか？」
- Record on any phone app. Walk out with an audio file.

### Step 2: Transcribe (15 min)
- Use Whisper API (language=ja) or local whisper large-v3
- Output: Japanese transcript text file

### Step 3: Generate Report (30 min)
- Paste transcript into the prompt from PROCESSING-PROMPT.md
- Use Claude or GPT-4

### Step 4: Self-Evaluate (15 min)
| Question | Y/N | Notes |
|---|---|---|
| Transcript accurate? Medical terms correct? | | |
| Section 1 (Visit Summary) reflects what happened? | | |
| Section 2 (Key Medical Info) captures right data? | | |
| Section 3 (Next Visit Prep) identifies real unresolved topics? | | |
| Japanese register appropriate for doctor? | | |
| Anything factually wrong? | | |
| Comfortable sharing with doctor? | | |
| Would you pay ¥1,500/month for this? | | |

### Step 5: Add Patient Notes
Fill in Section 4 with your own additions.

### Step 6: Share With Doctor (Next Visit)
- Print or email the report
- Ask: 「前回の診察の内容をAIでまとめたものです。次回の参考になればと思いまして。」
- Get feedback: Was it accurate? Useful? Would they want it regularly?

### Step 7: Record Results
Document transcription quality, report quality (1-10 per section), doctor feedback, and personal assessment.

## Decision Gate
- Report accurate AND doctor finds it useful → Proceed to expanded validation
- Report accurate BUT doctor doesn't find it useful → Redesign report
- Report NOT accurate → Investigate transcription vs. analysis quality

## Timeline
- Day 0: Set up Whisper
- Day 1-14: Attend appointment, record
- Same day: Transcribe + generate + self-evaluate
- Day 15-30: Share with doctor at next visit, get feedback
- Total active work: ~2 hours
