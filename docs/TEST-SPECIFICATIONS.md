# Kenkoumon — Test Specifications

## Overview

This document specifies the testing approach for Kenkoumon, incorporating TDD (Test-Driven Development) and BDD (Behavior-Driven Development) methodologies across all development phases.

---

## Testing Pyramid

```
                   /\
                  /  \
                 / E2E \  ← 10% (Critical journeys, BDD)
                /------\
               /        \
              /Integration\ ← 30% (API contracts, BDD)
             /------------\
            /              \
           /    Unit Tests   \ ← 60% (Business logic, TDD)
          /------------------\
```

---

## Phase 0: Experiment Zero (Manual Validation)

### Test Approach

**Type:** Manual testing with structured evaluation

**Test Artifacts:**
- [docs/SCORECARD-TEMPLATE.md](SCORECARD-TEMPLATE.md) - Evaluation rubric
- [docs/AI-COMPARISON.md](AI-COMPARISON.md) - Performance comparison matrix

### Test Scenarios

#### Scenario 1: Transcription Accuracy
```gherkin
Feature: Japanese Medical Transcription

  Scenario: Transcribe with local Whisper
    Given a Japanese medical consultation audio file
    And the audio contains 5+ medication names
    When I transcribe with local Whisper
    Then medical terms should be transcribed with >85% accuracy
    And processing should complete in <2 minutes for 10-minute audio
```

#### Scenario 2: Report Quality
```gherkin
Feature: Medical Report Generation

  Scenario: Generate structured doctor report
    Given a Japanese transcript of a medical consultation
    And the transcript contains medications, conditions, and instructions
    When I generate a report using Ollama/Llama
    Then the report should contain all 4 required sections
    And medications should be extracted with dosage information
    And the Japanese register should be appropriate for doctors
```

#### Scenario 3: Full Pipeline
```gherkin
Feature: End-to-End Processing

  Scenario: Process audio to shareable report
    Given a recorded medical consultation audio file
    When I run the full pipeline
    Then a timestamped directory should be created
    And it should contain: transcript, report, scorecard
    And total processing should be <10 minutes
```

### Validation Checklist

| Aspect | Test Method | Success Criteria |
|--------|-------------|------------------|
| Transcription accuracy | Manual comparison | >85% medical terms |
| Report completeness | Section review | All 4 sections present |
| Japanese quality | Native speaker review | Appropriate register |
| Processing time | Stopwatch | <10 minutes total |
| Doctor feedback | Doctor interview | Finds it useful |

---

## Phase 1: Repository Scaffolding (M3)

### Test Approach

**Type:** Automated TDD with some integration tests

**Frameworks:**
- Mobile: Jest + React Native Testing Library / Flutter Test
- Backend: pytest (Python) or Jest (Node.js)

### Unit Tests (TDD)

#### Transcription Service
```typescript
describe('TranscriptionService', () => {
  describe('source selection', () => {
    it('should use on-device whisper.cpp when source="on-device"', () => {
      const service = new TranscriptionService({ source: 'on-device' });
      expect(service.provider).toBe('OnDeviceWhisperService');
    });

    it('should fallback to cloud when on-device fails', async () => {
      const service = new TranscriptionService({
        source: 'on-device',
        fallback: true
      });
      // Mock on-device failure
      jest.spyOn(service.onDevice, 'transcribe').mockRejectedValue(new Error());
      const result = await service.transcribe(audio);
      expect(result.provider).toBe('cloud');
    });
  });

  describe('transcribe()', () => {
    it('should return Japanese text', async () => {
      const service = new TranscriptionService({ source: 'api' });
      const result = await service.transcribe(testAudio);
      expect(result.text).toBeDefined();
      expect(result.language).toBe('ja');
    });

    it('should handle API timeouts gracefully', async () => {
      const service = new TranscriptionService({ source: 'api' });
      jest.spyOn(service.api, 'transcribe').mockImplementation(() =>
        new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), 31000))
      );
      await expect(service.transcribe(audio)).rejects.toThrow('timeout');
    });
  });
});
```

### Integration Tests (BDD)

```gherkin
Feature: AI Source Selection

  Scenario: Switch between AI sources
    Given the app is configured for on-device AI
    When I change to user-hosted AI
    Then transcription should use the Ollama endpoint
    And report generation should use the Ollama endpoint

  Scenario: Automatic fallback
    Given on-device AI is not available
    And fallback is enabled
    When I process a recording
    Then it should automatically use cloud AI
    And I should be notified of the fallback
```

---

## Phase 2: Core Pipeline (M4-M7)

### Mobile App Tests

#### Framework: Detox (React Native) / Espresso (Flutter)

```gherkin
Feature: Audio Recording (F1)

  Scenario: Record medical consultation
    Given I am on the recording screen
    When I tap "Start Recording"
    Then a timer should display showing elapsed time
    And a "Stop Recording" button should appear
    When I tap "Stop Recording"
    Then the recording should stop
    And audio should be saved in m4a format
    And I should see a "Processing" option

  Scenario: Handle recording interruption
    Given I am recording
    When a phone call comes in
    Then recording should pause
    And I should be prompted to resume or stop
```

#### Backend API Tests

```gherkin
Feature: Transcription Pipeline (F2)

  Scenario: Upload and transcribe audio
    Given I have a recorded audio file
    And I am authenticated
    When I upload the audio to /sessions
    Then the response should include a session_id
    And the session status should be "uploading"
    When the upload completes
    Then the status should change to "uploaded"
    And a transcription job should start
    And the status should change to "transcribing"
    When transcription completes
    Then the status should be "transcribed"
    And the transcript_ja field should be populated

  Scenario: Handle transcription failure
    Given a transcription job fails
    When the error is detected
    Then the status should be "transcription_failed"
    And an error message should be logged
    And the user should be notified
```

```gherkin
Feature: Report Generation (F3)

  Scenario: Generate report from transcript
    Given a session with status "transcribed"
    And the transcript contains medical information
    When the report generation job runs
    Then entities should be extracted:
      | medications | conditions | instructions | providers |
    And a report should be generated with 4 sections
    And entities should be stored in their respective tables
    And the session status should be "complete"

  Scenario: Extract medication with dosage
    Given a transcript mentions "アタババルチン 10mg 1日3回"
    When the entity extractor runs
    Then a medication should be created:
      | name_ja | name_en | dosage | status |
      | アタババルチン | Atorvastatin | 10mg | discussed |
```

### Security Tests

```gherkin
Feature: Encryption (M7)

  Scenario: Encrypt audio at rest
    Given a user uploads audio
    When the audio is stored
    Then it should be encrypted with AES-256
    And each user should have a unique encryption key

  Scenario: TLS 1.3 in transit
    Given the mobile app communicates with the backend
    When any data is transmitted
    Then it should use TLS 1.3
    And the app should reject non-TLS connections

  Scenario: Patient data isolation
    Given user A and user B have sessions
    When user A requests their sessions
    Then they should see only their own sessions
    And user B's sessions should not be accessible
```

---

## Performance Tests

### Benchmarks

| Metric | Target | Test Method |
|--------|--------|-------------|
| Transcription (local) | <2 min / 10 min audio | Stopwatch |
| Report generation (local) | <3 min / transcript | Stopwatch |
| Full pipeline | <5 min total | Stopwatch |
| Audio upload | <30s / 10MB file | Network profiling |
| API response time | p95 <500ms | Load testing |

### Load Tests

```typescript
describe('Load Tests: Report Generation', () => {
  it('should handle 10 concurrent report generations', async () => {
    const promises = Array(10).fill().map(() =>
      api.generateReport(transcript)
    );
    const results = await Promise.all(promises);
    results.forEach(r => expect(r.status).toBe(200));
  });
});
```

---

## Accessibility Tests

### WCAG 2.1 AA Compliance

| Aspect | Test | Success Criteria |
|--------|------|------------------|
| Color contrast | Automated scan | >4.5:1 for text |
| Touch targets | Manual review | Min 44x44px |
| Screen reader | VoiceOver test | Navigable without vision |
| Font sizing | Manual review | Scalable to 200% |
| Japanese text | Native review | Readable, appropriate fonts |

---

## Test Data Strategy

### Synthetic Test Data

```typescript
// Test transcripts with known medical entities
const TEST_TRANSCRIPTS = {
  simple: "血圧が高めです。薬はアタババルチンを出しました。",
  complex: `
    高血圧と高コレステロールがあります。
    アタババルチン 10mg を朝食後に1錠。
    ロスバスタチン 5mg を夕食後に1錠。
    来月までに血液検査をしてください。
    禁煙もお願いします。
  `,
  edge_cases: [
    "Only medications mentioned",
    "Only instructions, no diagnosis",
    "Multiple doctors discussed",
    "No clear medical information"
  ]
};
```

### Test Audio Files

| File | Duration | Characteristics | Purpose |
|------|----------|----------------|--------|
| `sample-01.m4a` | 2 min | Clear audio, 1 doctor, 3 meds | Basic test |
| `sample-02.m4a` | 5 min | Background noise, 2 doctors | Noise robustness |
| `sample-03.m4a` | 10 min | Complex case, 5+ meds, tests | Full extraction |
| `sample-04.m4a` | 1 min | Mumbling, quiet audio | Edge case |
| `sample-05.m4a` | 15 min | Long consultation | Performance test |

---

## Continuous Testing

### Pre-Commit Hooks

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run fast tests
npm run test:unit -- --changedSince HEAD

# Run linter
npm run lint

# Type check
npm run type-check

# Security scan
npm audit --production
```

### CI Pipeline

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run test:unit -- --coverage

  integration:
    runs-on: ubuntu-latest
    services:
      - postgres
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run test:integration

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm audit --production
      - uses: snyk/actions/node@master
```

---

## Definition of Done for Tests

### Before Code is "Done"

| Test Type | Requirement |
|-----------|------------|
| Unit | All new code has unit tests |
| Integration | New features have integration tests |
| BDD | User stories have behavior scenarios |
| Coverage | >80% for new code |
| Security | No critical vulnerabilities |
| Performance | Meets NFRs on target hardware |

### Test Review Checklist

- [ ] Tests written before implementation (TDD)
- [ ] BDD scenarios cover acceptance criteria
- [ ] Tests are readable and maintainable
- [ ] Tests run in CI without manual intervention
- [ ] Test data is realistic and varied
- [ ] Edge cases are covered

---

## References

- [docs/DEFINITION-OF-DONE.md](DEFINITION-OF-DONE.md) - Milestone completion criteria
- [docs/MVP-SPEC.md](MVP-SPEC.md) - Feature specifications
- [docs/ARCHITECTURE.md](ARCHITECTURE.md) - Technical design
