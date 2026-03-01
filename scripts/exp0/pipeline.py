#!/usr/bin/env python3
"""
Kenkoumon Experiment Zero - End-to-End Pipeline

Chains transcription and report generation:
audio file → transcript → report → timestamped output directory

Usage:
    python pipeline.py recording.m4a [--transcribe-source local|api] [--llm-provider ollama|claude|openai]

Output directory structure:
    runs/YYYY-MM-DD-doctor/
    ├── recording.m4a          (original audio, optional copy)
    ├── transcript.txt         (Japanese transcript)
    ├── report.md              (structured doctor report)
    └── scorecard.md           (blank evaluation template)
"""

import argparse
import os
import shutil
import sys
import subprocess
from datetime import datetime
from pathlib import Path

# Default paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
RUNS_DIR = PROJECT_ROOT / "runs"
SCORECARD_TEMPLATE = PROJECT_ROOT / "docs" / "SCORECARD-TEMPLATE.md"

def create_session_dir(doctor_name: str = "doctor") -> Path:
    """Create timestamped session directory."""
    today = datetime.now().strftime("%Y-%m-%d")
    session_name = f"{today}-{doctor_name}"
    session_dir = RUNS_DIR / session_name

    session_dir.mkdir(parents=True, exist_ok=True)
    print(f"Session directory: {session_dir}")
    return session_dir

def run_transcription(audio_path: Path, session_dir: Path, source: str = "local") -> Path:
    """Run transcription script."""
    print("\n" + "="*60)
    print("STEP 1: Transcription")
    print("="*60)

    transcript_path = session_dir / "transcript.txt"

    # Build command
    script_path = SCRIPT_DIR / "transcribe.py"
    cmd = [
        "python", str(script_path),
        str(audio_path),
        "--source", source,
        "--output", str(transcript_path)
    ]

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False)

    if result.returncode != 0:
        print("Error: Transcription failed")
        return None

    print(f"Transcript saved to: {transcript_path}")
    return transcript_path

def run_report_generation(transcript_path: Path, session_dir: Path, provider: str = "ollama") -> Path:
    """Run report generation script."""
    print("\n" + "="*60)
    print("STEP 2: Report Generation")
    print("="*60)

    report_path = session_dir / "report.md"

    # Build command
    script_path = SCRIPT_DIR / "generate_report.py"
    cmd = [
        "python", str(script_path),
        str(transcript_path),
        "--provider", provider,
        "--output", str(report_path)
    ]

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False)

    if result.returncode != 0:
        print("Error: Report generation failed")
        return None

    print(f"Report saved to: {report_path}")
    return report_path

def create_scorecard(session_dir: Path):
    """Copy scorecard template to session directory."""
    print("\n" + "="*60)
    print("STEP 3: Scorecard Template")
    print("="*60)

    scorecard_path = session_dir / "scorecard.md"

    if SCORECARD_TEMPLATE.exists():
        shutil.copy(SCORECARD_TEMPLATE, scorecard_path)
        print(f"Scorecard template copied to: {scorecard_path}")
    else:
        print(f"Warning: Scorecard template not found at {SCORECARD_TEMPLATE}")
        # Create minimal placeholder
        scorecard_path.write_text("# Scorecard - To be filled\n")
        print(f"Placeholder scorecard created at: {scorecard_path}")

    return scorecard_path

def copy_audio(audio_path: Path, session_dir: Path):
    """Optionally copy original audio to session directory."""
    dest_path = session_dir / audio_path.name
    shutil.copy(audio_path, dest_path)
    print(f"Audio copied to: {dest_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Kenkoumon Experiment Zero - Full Pipeline"
    )
    parser.add_argument(
        "audio_file",
        help="Path to audio file (m4a, wav, mp3)"
    )
    parser.add_argument(
        "--doctor",
        default="doctor",
        help="Doctor identifier for session directory (default: doctor)"
    )
    parser.add_argument(
        "--transcribe-source",
        choices=["local", "api"],
        default="local",
        help="Transcription source (default: local)"
    )
    parser.add_argument(
        "--llm-provider",
        choices=["ollama", "claude", "openai"],
        default="ollama",
        help="LLM provider for report generation (default: ollama)"
    )
    parser.add_argument(
        "--llm-model",
        help="Specific model name (provider-specific)"
    )
    parser.add_argument(
        "--no-audio-copy",
        action="store_true",
        help="Don't copy original audio to session directory"
    )

    args = parser.parse_args()

    # Validate input
    audio_path = Path(args.audio_file)
    if not audio_path.exists():
        print(f"Error: Audio file not found: {args.audio_file}")
        sys.exit(1)

    print("="*60)
    print("Kenkoumon Experiment Zero Pipeline")
    print("="*60)
    print(f"Audio: {audio_path.name}")
    print(f"Transcription: {args.transcribe_source}")
    print(f"Report Generation: {args.llm_provider}")

    # Create session directory
    session_dir = create_session_dir(args.doctor)

    # Optionally copy audio
    if not args.no_audio_copy:
        copy_audio(audio_path, session_dir)

    # Step 1: Transcribe
    transcript_path = run_transcription(audio_path, session_dir, args.transcribe_source)
    if not transcript_path:
        sys.exit(1)

    # Step 2: Generate report
    report_path = run_report_generation(transcript_path, session_dir, args.llm_provider)
    if not report_path:
        sys.exit(1)

    # Step 3: Create scorecard
    scorecard_path = create_scorecard(session_dir)

    # Summary
    print("\n" + "="*60)
    print("PIPELINE COMPLETE")
    print("="*60)
    print(f"\nSession directory: {session_dir}")
    print(f"\nOutput files:")
    print(f"  - transcript.txt")
    print(f"  - report.md")
    print(f"  - scorecard.md")
    if not args.no_audio_copy:
        print(f"  - {audio_path.name}")

    print(f"\nNext steps:")
    print(f"  1. Review the transcript for accuracy")
    print(f"  2. Review the report for quality")
    print(f"  3. Fill out the scorecard")
    print(f"  4. Share report with doctor at next visit")

if __name__ == "__main__":
    main()
