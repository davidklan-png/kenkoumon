# User Guide

Complete guide for using Kenkoumon to record, process, and share medical consultation reports.

## Table of Contents

- [First-Time Setup](#first-time-setup)
- [Recording a Consultation](#recording-a-consultation)
- [Processing a Recording](#processing-a-recording)
- [Reviewing & Editing](#reviewing--editing)
- [Sharing with Your Doctor](#sharing-with-your-doctor)
- [Managing Sessions](#managing-sessions)
- [Settings](#settings)

---

## First-Time Setup

### 1. Create Account

Upon opening the app, you'll be prompted to create an account:

1. Enter your email address
2. Create a password (min 8 characters)
3. Enter your name (optional)
4. Tap "Create Account"

### 2. Configure AI Source

Choose how your recordings are processed:

**On-Device (Most Private)**
- AI runs entirely on your phone
- No data leaves your device
- Requires iPhone 14+ or newer
- First run downloads AI models (~4GB)

**User-Hosted (Balanced)**
- AI runs on your home server
- Requires Ollama or similar set up
- Enter your server URL

**Cloud (Best Quality)**
- AI runs on cloud services
- Requires API keys (OpenAI, Anthropic)
- Data encrypted in transit

### 3. Configure Recording Settings

1. Tap **Settings** gear icon
2. Choose audio format (M4A recommended)
3. Set language (Japanese)
4. Configure quality (High recommended)

---

## Recording a Consultation

### Before Your Appointment

1. Open Kenkoumon
2. Tap **Record** button (microphone icon)
3. Confirm you have permission to record
4. Ask your doctor: 「すみません、自分の記録のために会話を録音してもよろしいでしょうか？」

### Recording

1. Tap **Start Recording**
2. Place phone near you and your doctor
3. Timer will show elapsed time
4. Tap **Stop Recording** when finished

### Tips for Good Recordings

- **Position:** Place phone on table between you and doctor
- **Volume:** Speak normally; don't shout
- **Noise:** Avoid noisy environments if possible
- **Interruptions:** If interrupted, the app pauses automatically

---

## Processing a Recording

After stopping, choose:

### Process Immediately

1. Tap **Process Now**
2. Choose AI source (if not set in settings)
3. Processing happens in background
4. You'll be notified when complete (~2-5 minutes)

**Status Updates:**
- Uploading → Transcribing → Generating → Complete

### Review Later

1. Tap **Review Later**
2. Recording is saved to session history
3. Process anytime from **Sessions** list

---

## Reviewing & Editing

### Viewing the Report

1. From **Sessions**, tap a completed session
2. Report shows 4 sections:

**Section 1: 診察内容の要約** (Visit Summary)
- Summary of what was discussed
- Read-only, AI-generated

**Section 2: 主な医療情報** (Key Medical Information)
- Medications with dosages
- Conditions/diagnoses
- Tests ordered
- Read-only, AI-generated

**Section 3: 次回診察に向けて** (Next Visit Prep)
- Instructions to follow
- Follow-up items
- Read-only, AI-generated

**Section 4: 患者からのメモ** (Your Notes)
- **Editable** - add your own notes
- Auto-saves as you type
- Shareable with doctor

### Editing Your Notes

1. Tap in **Section 4** area
2. Type your notes in Japanese or English
3. Notes auto-save
4. Tap **Done** when finished

### Fact-Checking

Review the AI-generated content for accuracy:
- Medication names and dosages
- Condition names
- Instructions

If something seems wrong, add a note in Section 4.

---

## Sharing with Your Doctor

### Create Share Link

1. From report view, tap **Share**
2. Choose expiration (default: 30 days)
3. Tap **Create Link**
4. Link is automatically copied

### Share Options

**Copy Link**
- Link copied to clipboard
- Paste in email, LINE, etc.

**QR Code**
- Show QR code to doctor
- Doctor scans with phone camera

**Print**
- Generate PDF
- Print or save as PDF

### What Your Doctor Sees

Your doctor sees:
- Full report in Japanese
- Your notes (Section 4)
- No personal account information
- No audio recording

### Sharing at Your Next Visit

1. Open the shared link on your phone
2. Show to your doctor
3. Say: 「前回の診察の内容をAIでまとめたものです。次回の参考になればと思いまして。」

---

## Managing Sessions

### Session List

From **Sessions** tab, you'll see:

| Date | Doctor/Clinic | Status | Actions |
|------|--------------|--------|---------|
| Mar 1 | 田中クリニック | Complete | View, Share, Delete |
| Feb 15 | 山田病院 | Complete | View, Share, Delete |
 | Feb 1 | 佐々木医院 | Uploaded | Process, Delete |

### Session Actions

**View Report**
- Tap any session to view full report

**Delete Audio**
- Keeps transcript and report
- Removes audio file (saves space)
- Tap session → Delete Audio

**Delete Session**
- Permanently removes all data
- Cannot be undone
- Tap session → Delete Session

### Searching

- Scroll through chronological list
- Search by doctor name (future feature)
- Filter by date range (future feature)

---

## Settings

### AI Settings

**Transcription Source**
- On-device / User-hosted / Cloud
- Configure API keys or server URL

**Report Generation**
- On-device / User-hosted / Cloud
- Choose provider (Claude, GPT-4, Llama)

### Recording Settings

**Audio Format**
- M4A (recommended, smaller size)
- WAV (higher quality, larger size)

**Audio Quality**
- High (recommended)
- Medium
- Low (saves space)

**Language**
- Japanese (default)
- English

### Account Settings

**Email**
- Cannot be changed
- Used for login

**Password**
- Tap Change Password
- Enter current password
- Enter new password (twice)

**Delete Account**
- Permanently deletes all data
- Cannot be undone
- Confirmation required

### Storage Settings

**Manage Storage**
- View audio storage used
- Delete old audio files
- Keep transcripts/reports

**Auto-Delete Audio**
- Off (keep all)
- After 30 days
- After 90 days

### Privacy Settings

**Analytics**
- Disabled by default
- No personal data collected

**Crash Reports**
- Optional, helps improve app

---

## Tips & Best Practices

### Before Recording

- ✅ Charge your phone (>50%)
- ✅ Test microphone in settings
- ✅ Clear storage space (1GB+ recommended)
- ✅ Ask permission to record

### During Recording

- ✅ Place phone on table between you and doctor
- ✅ Speak clearly and naturally
- ✅ Don't hide phone under papers
- ❌ Don't switch apps during recording

### After Recording

- ✅ Process while on WiFi (if using cloud)
- ✅ Review report for accuracy
- ✅ Add your own notes
- ✅ Share before next appointment

### Sharing

- ✅ Share 1-2 days before appointment
- ✅ Print backup copy
- ✅ Ask doctor for feedback

---

## Troubleshooting

### Recording Won't Start

**Microphone Permission Denied:**
1. Go to iOS Settings > Kenkoumon
2. Enable Microphone
3. Restart app

**Storage Full:**
1. Delete old recordings
2. Offload photos/videos
3. Clear app cache

### Processing Fails

**Network Error:**
1. Check internet connection
2. Try again later
3. Switch to on-device processing

**API Key Invalid:**
1. Check Settings > AI Configuration
2. Verify API key is correct
3. Check billing status

### Report Quality Poor

**Medical Terms Wrong:**
- AI may mishear medical terms
- Add corrections in Section 4
- Choose higher quality recording

**Missing Information:**
- Doctor may have spoken quietly
- Try positioning phone closer
- Add missing info in Section 4

---

## Privacy & Security

### Data Storage

- **Audio:** Encrypted AES-256 at rest
- **Transcripts:** Encrypted per-patient
- **Reports:** Encrypted per-patient

### Data Sharing

- **You control** all data
- **Share links** expire automatically
- **Doctor access** is read-only
- **No data sold** to third parties

### Your Rights

- **Export:** Request all your data
- **Delete:** Delete account anytime
- **Access:** View all stored data

---

## Getting Help

### In-App Help

- Tap **Help** in settings
- View FAQ
- Contact support

### Feedback

We welcome feedback on:
- Report quality
- App usability
- Feature requests
- Bug reports

Email: support@kenkoumon.example.com

---

## Disclaimer

Kenkoumon is a **wellness tool**, not a medical device.

- Reports are AI-generated and may contain errors
- Always verify medical information with your doctor
- Do not rely on Kenkoumon for medical decisions
- Consult qualified healthcare professionals

---

## Quick Reference

| Task | Steps |
|------|-------|
| **Record** | Record → Stop → Process Now |
| **Review** | Sessions → Tap session → Read report |
| **Edit Notes** | Section 4 → Type → Auto-saves |
| **Share** | Share → Choose expiration → Copy link |
| **Delete Audio** | Session → Delete Audio |
| **Delete Session** | Session → Delete Session |
