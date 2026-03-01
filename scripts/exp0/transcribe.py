#!/usr/bin/env python3
"""
Kenkoumon Experiment Zero - Transcription Script

Transcribes Japanese audio files using either:
1. Local Whisper (whisper.cpp or openai-whisper)
2. OpenAI Whisper API (cloud fallback)

Usage:
    python transcribe.py recording.m4a [--source local|api] [--model base|small|medium]

Requirements:
    - For local: pip install openai-whisper
    - For API: OPENAI_API_KEY environment variable
"""

import argparse
import os
import sys
from pathlib import Path

def transcribe_local(audio_path: str, model_size: str = "base") -> str:
    """Transcribe using local Whisper model."""
    try:
        import whisper
    except ImportError:
        print("Error: openai-whisper not installed.")
        print("Install with: pip install openai-whisper")
        sys.exit(1)

    print(f"Loading local Whisper model: {model_size}")
    model = whisper.load_model(model_size)

    print(f"Transcribing: {audio_path}")
    result = model.transcribe(
        audio_path,
        language="ja",
        task="transcribe",
        verbose=False
    )

    return result["text"]

def transcribe_api(audio_path: str) -> str:
    """Transcribe using OpenAI Whisper API."""
    try:
        from openai import OpenAI
    except ImportError:
        print("Error: openai package not installed.")
        print("Install with: pip install openai")
        sys.exit(1)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)

    client = OpenAI()

    print(f"Transcribing via API: {audio_path}")
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="ja",
            response_format="text"
        )

    return transcript

def main():
    parser = argparse.ArgumentParser(
        description="Transcribe Japanese audio to text"
    )
    parser.add_argument(
        "audio_file",
        help="Path to audio file (m4a, wav, mp3)"
    )
    parser.add_argument(
        "--source",
        choices=["local", "api"],
        default="local",
        help="Transcription source (default: local)"
    )
    parser.add_argument(
        "--model",
        choices=["tiny", "base", "small", "medium", "large"],
        default="base",
        help="Local model size (default: base)"
    )
    parser.add_argument(
        "--output",
        help="Output transcript path (default: audio_file.txt)"
    )

    args = parser.parse_args()

    # Validate input file
    audio_path = Path(args.audio_file)
    if not audio_path.exists():
        print(f"Error: Audio file not found: {args.audio_file}")
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = audio_path.with_suffix(".txt")

    # Transcribe
    if args.source == "local":
        transcript = transcribe_local(str(audio_path), args.model)
    else:
        transcript = transcribe_api(str(audio_path))

    # Write output
    output_path.write_text(transcript, encoding="utf-8")
    print(f"\nTranscript saved to: {output_path}")

if __name__ == "__main__":
    main()
