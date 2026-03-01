# Claude Code Prompt — Initialize Kenkoumon Repository

Copy and paste the following prompt into Claude Code:

---

```
I need you to create a new GitHub repository and push project files to it.

## Repository Details
- Name: Kenkoumon
- Description: "Patient-owned medical session intelligence platform. Records doctor-patient consultations, produces structured bilingual reports, builds longitudinal health profiles."
- Visibility: Private
- No template

## Steps
1. Check if `gh` CLI is authenticated. If not, guide me through authentication.
2. Create the repo on GitHub using `gh repo create Kenkoumon --private --description "Patient-owned medical session intelligence platform. Records doctor-patient consultations, produces structured bilingual reports, builds longitudinal health profiles."`
3. Initialize a local git repo in the current directory
4. Copy all .md files and .gitignore from the provided project files into the repo
5. Create an initial commit with message: "Initial project architecture and Experiment Zero protocol"
6. Push to main branch

## Project Files to Include
The following files should already be in my working directory (I'll upload or paste them):

- README.md
- ARCHITECTURE.md
- EXPERIMENT-ZERO.md
- DOCTOR-REPORT-SPEC.md
- PROCESSING-PROMPT.md
- VISION.md
- RISKS.md
- BUSINESS-MODEL.md
- DECISIONS-LOG.md
- .gitignore

If the files aren't present, let me know and I'll provide them.

## After Repo Creation
- Confirm the repo URL
- Verify all files are pushed
- Create a GitHub Issue titled "Experiment Zero: First Doctor Visit" with the following body:

---
## Objective
Record first doctor-patient consultation and validate core hypothesis.

## Checklist
- [ ] Set up Whisper (API key or local install)
- [ ] Schedule/attend doctor appointment
- [ ] Ask permission to record
- [ ] Record consultation
- [ ] Transcribe Japanese audio with Whisper
- [ ] Run transcript through processing prompt (see PROCESSING-PROMPT.md)
- [ ] Self-evaluate report quality
- [ ] Add patient notes to Section 4
- [ ] Share report with doctor at next visit
- [ ] Record doctor feedback

## Decision Gate
- If report is accurate AND doctor finds it useful → proceed to expanded validation
- If report is accurate BUT doctor doesn't find it useful → redesign report
- If report is NOT accurate → investigate transcription vs. analysis quality
---
```

---

## Alternative: If Files Need to Be Created Inline

If you haven't downloaded the project files, use this modified prompt that tells Claude Code to create them:

```
Create a new private GitHub repo called "Kenkoumon" with description "Patient-owned medical session intelligence platform." Then create all project documentation files from the specifications I'll paste below, commit them, and push to main. Also create a GitHub Issue for Experiment Zero tracking.
```

Then paste the contents of each .md file when prompted.
