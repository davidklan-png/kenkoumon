# Kenkoumon — Definition of Done (DoD)

## Overview

This document defines the Definition of Done for each milestone and phase of the Kenkoumon project. It incorporates Test-Driven Development (TDD) and Behavior-Driven Development (BDD) principles to ensure quality at every stage.

## DoD Hierarchy

```
Project DoD (All Milestones)
    ├── Milestone DoD (Specific to M1-M8)
    │   ├── Feature DoD (Per User Story)
    │   └── Sprint DoD (Per Development Iteration)
    └── Acceptance Criteria (Per Issue/Ticket)
```

---

## Project-Level Definition of Done

Applies to **all milestones** and **all deliverables**.

### Quality Gates

| Category | Criteria | Verification |
|----------|----------|---------------|
| **Testing** | All tests passing | CI/CD pipeline |
| **Documentation** | Updated for all changes | Manual review |
| **Code Review** | At least one approval | PR review process |
| **Security** | No critical vulnerabilities | Automated scan + review |
| **Performance** | Meets NFRs | Profiling/benchmarking |
| **Accessibility** | Core flows usable | Manual testing |
| **Japanese Support** | All UI text in Japanese | Review by native speaker |
| **Privacy** | APPI compliant | Legal review (M2+) |

### Deliverable Standards

- **Code:** Follows style guide, linted, commented where complex
- **Tests:** Unit tests for all logic, integration tests for flows
- **Docs:** README updated, API docs current
- **Changelog:** All user-facing changes noted

---

## Milestone-Level Definition of Done

### M1: Experiment Zero Tooling & Execution

#### Behavior Scenarios (BDD)

**Scenario 1: Transcribe Audio File**
```gherkin
GIVEN a Japanese audio recording of a medical consultation
WHEN I run the transcription script with local source
THEN the transcript should be saved as a text file
AND the transcript should contain Japanese text
AND medical terms should be transcribed with >80% accuracy
```

**Scenario 2: Generate Report from Transcript**
```gherkin
GIVEN a Japanese transcript of a medical consultation
AND the processing prompt template
WHEN I run the report generation script
THEN a structured report should be generated
AND the report should contain all 4 sections
AND entities should be extracted (medications, conditions, instructions)
```

**Scenario 3: Full Pipeline Execution**
```gherkin
GIVEN a recorded medical consultation audio file
WHEN I run the pipeline script
THEN a timestamped directory should be created
AND it should contain: transcript, report, scorecard
AND processing should complete in <10 minutes
```

#### Acceptance Criteria (Per Issue)

| Issue | DoD Checklist |
|-------|--------------|
| #2: Whisper transcription script | [ ] Handles m4a, wav, mp3<br>[ ] Outputs Japanese text<br>[ ] Configurable via env vars<br>[ ] Error handling for API failures<br>[ ] Tested with sample audio |
| #3: Report generation script | [ ] Reads transcript correctly<br>[ ] Uses processing prompt<br>[ ] Supports 3 LLM providers<br>[ ] Outputs 4-section report<br>[ ] Handles API timeouts |
| #4: Scorecard template | [ ] Covers all evaluation questions<br>[ ] Includes medical accuracy checks<br>[ ] Includes Japanese register assessment<br>[ ] Includes WTP question |
| #5: Pipeline script | [ ] Creates timestamped directory<br>[ ] Chains all steps<br>[ ] Handles errors gracefully<br>[ ] Copies audio to output |
| #6: Execute Experiment Zero | [ ] Recording obtained<br>[ ] Transcript generated<br>[ ] Report generated<br>[ ] Scorecard completed |
| #7: Share and get feedback | [ ] Report shared with doctor<br>[ ] Feedback documented<br>[ ] Go/no-go decision recorded |

#### Technical Tests (TDD)

```python
# Test: Transcription accuracy
def test_medical_term_accuracy():
    """Verify medical terms transcribed with >80% accuracy"""
    # Test with sample audio containing known medical terms
    # Compare transcription against reference
    assert accuracy >= 0.80

# Test: Report structure
def test_report_four_sections():
    """Verify report contains all 4 required sections"""
    report = generate_report(transcript)
    assert "診察内容の要約" in report
    assert "主な医療情報" in report
    assert "次回診察に向けて" in report
    assert "患者からのメモ" in report

# Test: Pipeline end-to-end
def test_pipeline_creates_output():
    """Verify pipeline creates expected output files"""
    output_dir = run_pipeline(test_audio)
    assert (output_dir / "transcript.txt").exists()
    assert (output_dir / "report.md").exists()
    assert (output_dir / "scorecard.md").exists()
```

#### Exit Criteria

- [ ] All 7 issues closed
- [ ] Scripts tested with real audio
- [ ] At least 1 complete Experiment Zero cycle executed
- [ ] Scorecard filled out
- [ ] Decision gate documented

---

### M2: Expanded Validation

#### Behavior Scenarios

**Scenario: Multi-User Validation**
```gherkin
GIVEN 5 expat testers with doctor appointments
WHEN they each use the pipeline for 2+ sessions
THEN we should collect 10+ scorecards
AND we should measure accuracy trends
AND we should identify >85% medical term accuracy threshold
```

#### Acceptance Criteria

| Issue | DoD Checklist |
|-------|--------------|
| Recruit 5 testers | [ ] 5 testers identified<br>[ ] Mix of visit types<br>[ ] Tracking set up |
| 10+ sessions | [ ] 10+ sessions processed<br>[ ] Scorecards collected<br>[ ] Accuracy documented |
| Doctor feedback | [ ] 3+ doctors feedback<br>[ ] >70% usefulness threshold met |
| Transcription alternatives | [ ] 2+ services evaluated<br>[ ] Comparison documented |
| LLM evaluation | [ ] Claude vs GPT-4 tested<br>[ ] Japan-region verified<br>[ ] Recommendation made |
| APPI legal consultation | [ ] Legal opinion obtained<br>[ ] Requirements documented<br>[ ] Architectural changes identified |
| Validation gate | [ ] All success criteria checked<br>[ ] Go/no-go decision made |

#### Exit Criteria

- [ ] All 7 issues closed
- [ ] Validation metrics met (>70% usefulness, >70% WTP)
- [ ] Transcription/LLM providers selected
- [ ] Legal consultation complete
- [ ] Go/no-go decision: PROCEED to M3

---

### M3: Repository Scaffolding

#### Behavior Scenarios

**Scenario: Mobile Framework Decision**
```gherkin
GIVEN React Native and Flutter options
WHEN evaluating against criteria (audio APIs, Japan SDK, productivity)
THEN a decision should be documented
AND rationale should be recorded in DECISIONS-LOG.md
```

**Scenario: AI Abstraction Layer**
```gherkin
GIVEN the AI abstraction requirement
WHEN implementing the service interfaces
THEN on-device, user-hosted, and cloud sources should be supported
AND switching should not require code changes
```

#### Acceptance Criteria

| Issue | DoD Checklist |
|-------|--------------|
| Framework decision | [ ] Criteria evaluated<br>[ ] Decision documented<br>[ ] DECISIONS-LOG.md updated |
| Mobile project | [ ] Builds on iOS + Android<br>[ ] Directory structure created<br>[ ] Placeholder screen shown |
| Backend API | [ ] Project initialized<br>[ ] Health check working<br>[ ] Dockerfile tested |
| PostgreSQL schema | [ ] All tables created<br>[ ] Migrations run successfully<br>[ ] UTF-8 for Japanese |
| CI pipeline | [ ] Runs on push<br>[ ] Green checks<br>[ ] Lint + type check + tests |
| AI abstraction layer | [ ] Interfaces defined<br>[ ] 3 source types supported<br>[ ] Provider swappable via config |

#### Technical Tests (TDD)

```typescript
// Test: AI abstraction layer
describe('TranscriptionService', () => {
  it('should switch between providers without code change', () => {
    const config = { source: 'on-device' };
    const service = new TranscriptionService(config);
    const result1 = service.transcribe(audio);

    config.source = 'cloud';
    const result2 = service.transcribe(audio);

    expect(result1).toBeDefined();
    expect(result2).toBeDefined();
  });
});
```

#### Exit Criteria

- [ ] All 6 issues closed
- [ ] CI pipeline running green
- [ ] Mobile app builds and runs
- [ ] Backend API health check responds
- [ ] Database schema applied

---

### M4: Core Pipeline — Record, Transcribe, Generate

#### Behavior Scenarios

**Scenario: Audio Recording (F1)**
```gherkin
GIVEN the app is open on the recording screen
WHEN I tap the record button
THEN recording should start
AND a timer should display
AND I can stop recording by tapping stop
AND audio is saved locally in m4a format
```

**Scenario: Transcription Pipeline (F2)**
```gherkin
GIVEN a recorded audio file
WHEN the audio is uploaded to backend
THEN it should be encrypted (AES-256)
AND status should change: uploading → uploaded → transcribing → transcribed
AND transcript should be stored in database
```

**Scenario: Report Generation (F3)**
```gherkin
GIVEN a completed transcript
AND the processing prompt
WHEN the report generation job runs
THEN a 4-section report should be generated
AND entities should be extracted to database
AND status should change: generating → complete
```

#### Acceptance Criteria

| Issue | DoD Checklist |
|-------|--------------|
| F1: Audio recording | [ ] Record/stop works<br>[ ] Timer displays<br>[ ] m4a format<br>[ ] On-device storage |
| Audio upload | [ ] Upload progress shown<br>[ ] Encrypted AES-256<br>[ ] Session created<br>[ ] Error handling |
| F2: Transcription | [ ] Audio → Japanese text<br>[ ] Medical terms accurate<br>[ ] Status updates work<br>[ ] Errors handled |
| F3: Report generation | [ ] 4 sections present<br>[ ] Entities extracted<br>[ ] Stored in DB<br>[ ] Status updates |
| Status polling | [ ] Real-time updates<br>[ ] 10-15s interval<br>[ ] Works in foreground |
| Time monitoring | [ ] Times logged per stage<br>[ ] <5 min total NFR |

#### Technical Tests (TDD)

```typescript
// Unit tests
describe('AudioRecorder', () => {
  it('should record audio in m4a format', () => {
    const recorder = new AudioRecorder();
    recorder.start();
    await delay(1000);
    const file = recorder.stop();
    expect(file.format).toBe('m4a');
  });
});

describe('TranscriptionPipeline', () => {
  it('should extract medical terms with >85% accuracy', async () => {
    const result = await pipeline.transcribe(medicalAudio);
    const accuracy = calculateMedicalAccuracy(result, reference);
    expect(accuracy).toBeGreaterThan(0.85);
  });
});

// Integration test
describe('End-to-End Pipeline', () => {
  it('should complete in <5 minutes on target device', async () => {
    const start = Date.now();
    await pipeline.run(testAudio);
    const duration = (Date.now() - start) / 1000 / 60;
    expect(duration).toBeLessThan(5);
  });
});
```

#### Exit Criteria

- [ ] All 6 issues closed
- [ ] End-to-end flow works on iOS + Android
- [ ] Processing <5 min on target device
- [ ] All tests passing

---

### M5: Patient Review & Notes (F4)

#### Behavior Scenarios

**Scenario: View Report**
```gherkin
GIVEN a generated report is ready
WHEN I open the report screen
THEN I should see all 4 sections in Japanese
AND Section 4 should be visually distinct (editable)
AND sections 1-3 should be read-only
```

**Scenario: Add Patient Notes**
```gherkin
GIVEN I am viewing a report
WHEN I type in Section 4
THEN my notes should auto-save
AND notes should persist across app restarts
```

**Scenario: Share Flow**
```gherkin
GIVEN processing is complete
WHEN I choose "share immediately"
THEN a secure link should be generated
WHEN I choose "review first"
THEN I should see the report
AND I can add notes before sharing
```

#### Acceptance Criteria

| Issue | DoD Checklist |
|-------|--------------|
| Report viewing | [ ] 4 sections render correctly<br>[ ] Japanese text proper<br>[ ] Section 4 distinct |
| Notes editing | [ ] Can type in Section 4<br>[ ] Auto-saves<br>[ ] Persists across restarts<br>[ ] Sections 1-3 read-only |
| Share flow | [ ] Both paths work<br>[ ] Immediate creates link<br>[ ] Review allows notes then share |
| Entities display | [ ] Structured format in Section 2<br>[ ] Bilingual labels shown<br>[ ] Medications include dosage |

#### Exit Criteria

- [ ] All 4 issues closed
- [ ] Share flow works both ways
- [ ] Doctor feedback positive on format

---

### M6: Secure Sharing & Auth (F5)

#### Behavior Scenarios

**Scenario: Patient Authentication**
```gherkin
GIVEN I am a new user
WHEN I create an account with email
THEN I should receive a verification email
AND I can log in with my credentials
AND I can only access my own data
```

**Scenario: Secure Link Generation**
```gherkin
GIVEN a completed report
WHEN I generate a secure link
THEN it should have a cryptographically random token
AND it should expire in 30 days by default
```

**Scenario: Public Report Viewing**
```gherkin
GIVEN a valid secure link URL
WHEN I open it in a browser
THEN I should see the full report in Japanese
AND no login should be required
WHEN the link is expired
THEN I should see an expiration message
```

#### Acceptance Criteria

| Issue | DoD Checklist |
|-------|--------------|
| Authentication | [ ] Account creation works<br>[ ] Email verification<br>[ ] JWT sessions<br>[ ] Password reset |
| Link generation | [ ] Cryptographically random<br>[ ] Expiration stored<br>[ ] Configurable duration |
| Public viewing | [ ] Valid link shows report<br>[ ] Expired shows message<br>[ ] Invalid shows 404<br>[ ] Responsive design |
| Link management | [ ] Expired blocked<br>[ ] Can revoke<br>[ ] Can view active |
| Share delivery | [ ] Copy to clipboard<br>[ ] System share sheet<br>[ ] QR code works |

#### Exit Criteria

- [ ] All 5 issues closed
- [ ] Auth flow works
- [ ] Secure links work
- [ ] Public page accessible

---

### M7: Session History & Encryption (F6)

#### Behavior Scenarios

**Scenario: View Session History**
```gherkin
GIVEN I have recorded multiple sessions
WHEN I open the session history screen
THEN I should see sessions sorted newest first
AND each session shows: date, provider, status
AND tapping should open the report
```

**Scenario: Delete Audio**
```gherkin
GIVEN a session with audio
WHEN I delete the audio
THEN the audio file should be removed
BUT the transcript and report should remain
```

#### Acceptance Criteria

| Issue | DoD Checklist |
|-------|--------------|
| Session history | [ ] Chronological list<br>[ ] Date, provider, status<br>[ ] Tap to view report<br>[ ] Smooth scrolling |
| AES-256 encryption | [ ] Per-patient keys<br>[ ] Key management works<br>[ ] Transparent decryption<br>[ ] Audio deletion |
| TLS 1.3 security | [ ] All connections TLS 1.3<br>[ ] HTTP → HTTPS<br>[ ] App rejects non-TLS |
| Japan-region deployment | [ ] All infra in Japan<br>[ ] No data transit outside<br>[ ] Documented |
| Audio deletion | [ ] Delete button exists<br>[ ] Transcript/report remain<br>[ ] Auto-delete option |

#### Exit Criteria

- [ ] All 5 issues closed
- [ ] Encryption implemented
- [ ] Japan-region deployed
- [ ] Security audit passed

---

### M8: Integration, Testing & Launch

#### Behavior Scenarios

**Scenario: End-to-End User Flow**
```gherkin
GIVEN I am a new user
WHEN I complete the full flow
THEN I should: record → process → review → share
AND the doctor should be able to view the report
AND the process should complete in <5 minutes
```

**Scenario: Error Handling**
```gherkin
GIVEN various error conditions (upload fails, API timeout)
WHEN errors occur
THEN they should be handled gracefully
AND I should see clear error messages
AND no sessions should be stuck
```

#### Acceptance Criteria

| Issue | DoD Checklist |
|-------|--------------|
| E2E testing | [ ] Both paths tested<br>[ ] Real audio tested<br>[ ] Both platforms<br>[ ] <5 min target<br>[ ] No blocking bugs |
| Disclaimers | [ ] Report disclaimer<br>[ ] Terms of service<br>[ ] Privacy policy<br>[ ] Wellness positioning |
| Metrics tracking | [ ] Sessions tracked<br>[ ] Share rate tracked<br>[ ] Survey triggerable<br>[ ] Metrics queryable |
| Error handling | [ ] All scenarios handled<br>[ ] No stuck sessions<br>[ ] Clear messages |
| TestFlight build | [ ] iOS installable<br>[ ] Android installable<br>[ ] Onboarding explains<br>[ ] Backend deployed |
| Launch to users | [ ] 10+ users have app<br>[ ] Sessions being recorded<br>[ ] Metrics collecting<br>[ ] Feedback loop active |

#### Exit Criteria

- [ ] All 6 issues closed
- [ ] 50+ sessions recorded
- [ ] >95% accuracy achieved
- [ ] >60% share rate achieved
- [ ] >70% retention achieved
- [ ] >50% doctor positive feedback
- [ ] >60% WTP achieved

---

## Feature-Level Definition of Done

Applies to each feature (F1-F6).

### Checklist

| Category | Criteria |
|----------|----------|
| **Behavior** | BDD scenarios written and passing |
| **Unit Tests** | All logic paths tested |
| **Integration** | Works with other features |
| **Documentation** | README/Docs updated |
| **Code Review** | Approved by peer |
| **Performance** | Meets NFRs |
| **Security** | No vulnerabilities |
| **Accessibility** | Usable by target users |

---

## Test Strategy (TDD/BDD)

### Three Levels of Testing

```
┌─────────────────────────────────────────┐
│         E2E Tests (BDD)                 │
│  User journeys, critical paths         │
│  Framework: Appium / Detox             │
└─────────────────────────────────────────┘
           ↑
┌─────────────────────────────────────────┐
│      Integration Tests (BDD)            │
│  Feature interactions, API contracts    │
│  Framework: Jest / XCTest Matchers     │
└─────────────────────────────────────────┘
           ↑
┌─────────────────────────────────────────┐
│        Unit Tests (TDD)                 │
│  Business logic, services, utilities    │
│  Framework: Jest / XCTest              │
└─────────────────────────────────────────┘
```

### Test Naming Conventions

**BDD (Behavior):**
```typescript
describe('Feature: Secure Link Sharing', () => {
  describe('Scenario: Generate secure link', () => {
    it('should create a link with random token', () => {
      // Test implementation
    });
  });
});
```

**TDD (Unit):**
```typescript
describe('SecureLinkService', () => {
  describe('generateToken()', () => {
    it('should return a cryptographically random string', () => {
      // Test implementation
    });
  });
});
```

---

## Continuous Integration

### CI Pipeline Requirements

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: macos-latest  # For iOS
    steps:
      - checkout
      - Install dependencies
      - Run unit tests
      - Run integration tests
      - Run linter
      - Run type check
      - Build app
```

### Quality Gates

| Gate | Tool | Threshold |
|------|------|-----------|
| Unit tests | Jest | 100% pass |
| Integration tests | Detox | 100% pass |
| Linting | ESLint | 0 errors |
| Type check | TypeScript | 0 errors |
| Coverage | Jest | >80% |
| Security | Snyk | 0 critical |

---

## Definition of Done vs Acceptance Criteria

| Aspect | DoD | Acceptance Criteria |
|--------|-----|---------------------|
| Scope | All work for milestone/feature | Specific to one user story |
| Timing | Checked at milestone completion | Checked when story is done |
| Ownership | Team/project level | Product owner/user |
| Examples | Tests passing, docs updated, security OK | User can record audio, report generates |

---

## References

- [docs/MVP-SPEC.md](MVP-SPEC.md) - Feature specifications
- [docs/EXPERIMENT-ZERO.md](EXPERIMENT-ZERO.md) - Validation protocol
- [docs/RISK-REGISTER.md](RISK-REGISTER.md) - Risk tracking
- [docs/ARCHITECTURE.md](ARCHITECTURE.md) - Technical design
