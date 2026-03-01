# Claude Code Prompt — Create Kenkoumon GitHub Repository

Copy and paste the following prompt into Claude Code to create the repository. Make sure you're authenticated with GitHub CLI (`gh auth status`) before running.

---

## Prompt

```
Create a new public GitHub repository called "Kenkoumon" with the description "健康門 — Patient-Owned Medical Visit Intelligence. Record doctor visits, generate AI-powered bilingual reports, own your health data."

Initialize it with the following structure and files. Read each file carefully and create them exactly as specified.

Repository structure:

Kenkoumon/
├── README.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── EXPERIMENT-ZERO.md
│   ├── VISION.md
│   ├── MVP-SPEC.md
│   ├── REPORT-TEMPLATE.md
│   └── RISK-REGISTER.md
├── experiments/
│   └── .gitkeep
└── .gitignore

The .gitignore should cover:
- Audio files (*.m4a, *.mp3, *.wav, *.ogg, *.flac)
- Transcripts that might contain PHI (keep templates only)
- Python/Node artifacts
- OS files (.DS_Store, Thumbs.db)
- Environment files (.env, .env.local)
- IDE files

All documentation files are already written and available in the /home/claude/kenkoumon/ directory. Copy them into the repository as-is.

The experiments/ directory is where Experiment Zero recordings, transcripts, and outputs will go (but audio files will be gitignored for privacy).

After creating the repo:
1. Create an initial commit with message "Initial project documentation from architecture design phase"
2. Push to GitHub
3. Create a GitHub Issue titled "Experiment Zero: First Recording" with this body:

"## Objective
Run the first live test of the Kenkoumon pipeline.

## Checklist
- [ ] Schedule or attend next doctor appointment
- [ ] Ask doctor for recording permission
- [ ] Record the consultation
- [ ] Transcribe Japanese audio (Whisper API or local)
- [ ] Generate doctor briefing using REPORT-TEMPLATE.md prompt
- [ ] Self-evaluate against criteria in EXPERIMENT-ZERO.md
- [ ] Document results in experiments/ directory
- [ ] Share report with doctor at next visit and collect feedback

## Success Criteria
See docs/EXPERIMENT-ZERO.md for full criteria.

## Blocking
All further development is blocked on this experiment's results."

4. Create a second GitHub Issue titled "Legal: APPI Preliminary Assessment" with this body:

"## Objective
Get preliminary legal opinion on APPI compliance for recording, transcribing, and storing medical consultation audio.

## Key Questions
- Does recording a medical consultation with verbal consent satisfy APPI requirements?
- What are the data residency requirements for medical audio and transcripts?
- Does the patient-owned data model simplify or complicate APPI compliance?
- What consent documentation is required?
- Are there specific requirements for AI processing of medical audio?

## Budget
¥200,000 - ¥500,000 for initial legal consultation

## Blocking
Must be resolved before any production deployment. Not blocking Experiment Zero (personal use)."

Confirm when the repository is created and both issues are filed.
```

---

## Prerequisites

Before running the Claude Code prompt:

1. **GitHub CLI authenticated:** Run `gh auth status` to verify
2. **Git configured:** Ensure `git config user.name` and `git config user.email` are set
3. **Files available:** The documentation files should be in `/home/claude/kenkoumon/` (or update paths in the prompt)

## After Repository Creation

1. Clone the repo locally: `gh repo clone [your-username]/Kenkoumon`
2. Review all documentation files for any adjustments specific to your situation
3. Begin Experiment Zero protocol (see docs/EXPERIMENT-ZERO.md)
