#!/usr/bin/env python3
"""
Kenkoumon Experiment Zero - Report Generation Script

Generates structured doctor reports from Japanese transcripts using:
1. Local LLM (Ollama)
2. Claude API (Anthropic)
3. OpenAI GPT-4 API

Usage:
    python generate_report.py transcript.txt [--provider ollama|claude|openai] [--model MODEL]

Requirements:
    - For Ollama: Ollama running locally with a model pulled
    - For Claude: ANTHROPIC_API_KEY environment variable
    - For OpenAI: OPENAI_API_KEY environment variable
"""

import argparse
import os
import sys
from pathlib import Path

# Default processing prompt
DEFAULT_PROMPT_PATH = Path(__file__).parent.parent.parent / "docs" / "PROCESSING-PROMPT.md"

def load_prompt(prompt_path: Path = None) -> str:
    """Load the processing prompt."""
    if prompt_path is None:
        prompt_path = DEFAULT_PROMPT_PATH

    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8")
    else:
        print(f"Warning: Prompt file not found: {prompt_path}")
        print("Using default prompt placeholder.")
        return "Generate a structured medical report from the following Japanese transcript."

def generate_report_ollama(transcript: str, prompt: str, model: str = "llama3.1") -> dict:
    """Generate report using local Ollama."""
    try:
        import requests
    except ImportError:
        print("Error: requests package not installed.")
        print("Install with: pip install requests")
        sys.exit(1)

    ollama_url = os.environ.get("OLLAMA_URL", "http://localhost:11434")

    # Combine prompt with transcript
    full_prompt = f"{prompt}\n\n## Transcript\n\n{transcript}"

    print(f"Calling Ollama: {model} at {ollama_url}")
    response = requests.post(
        f"{ollama_url}/api/generate",
        json={
            "model": model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 2048,
            }
        },
        timeout=300  # 5 minutes
    )
    response.raise_for_status()
    result = response.json()

    return {
        "content": result.get("response", ""),
        "model": model,
        "provider": "ollama"
    }

def generate_report_claude(transcript: str, prompt: str, model: str = "claude-sonnet-4-20250514") -> dict:
    """Generate report using Claude API."""
    try:
        from anthropic import Anthropic
    except ImportError:
        print("Error: anthropic package not installed.")
        print("Install with: pip install anthropic")
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)

    client = Anthropic(api_key=api_key)

    full_prompt = f"{prompt}\n\n## Transcript\n\n{transcript}"

    print(f"Calling Claude: {model}")
    message = client.messages.create(
        model=model,
        max_tokens=4096,
        temperature=0.3,
        messages=[{
            "role": "user",
            "content": full_prompt
        }]
    )

    return {
        "content": message.content[0].text,
        "model": model,
        "provider": "claude",
        "usage": message.usage.model_dump()
    }

def generate_report_openai(transcript: str, prompt: str, model: str = "gpt-4o") -> dict:
    """Generate report using OpenAI GPT-4 API."""
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

    client = OpenAI(api_key=api_key)

    full_prompt = f"{prompt}\n\n## Transcript\n\n{transcript}"

    print(f"Calling OpenAI: {model}")
    response = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": full_prompt
        }],
        max_tokens=4096,
        temperature=0.3
    )

    return {
        "content": response.choices[0].message.content,
        "model": model,
        "provider": "openai",
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
    }

def main():
    parser = argparse.ArgumentParser(
        description="Generate medical report from Japanese transcript"
    )
    parser.add_argument(
        "transcript_file",
        help="Path to transcript text file"
    )
    parser.add_argument(
        "--provider",
        choices=["ollama", "claude", "openai"],
        default="ollama",
        help="LLM provider (default: ollama)"
    )
    parser.add_argument(
        "--model",
        help="Model name (provider-specific)"
    )
    parser.add_argument(
        "--prompt",
        type=Path,
        default=None,
        help="Path to processing prompt (default: docs/PROCESSING-PROMPT.md)"
    )
    parser.add_argument(
        "--output",
        help="Output report path (default: transcript_file_report.md)"
    )

    args = parser.parse_args()

    # Validate input file
    transcript_path = Path(args.transcript_file)
    if not transcript_path.exists():
        print(f"Error: Transcript file not found: {args.transcript_file}")
        sys.exit(1)

    # Load transcript
    transcript = transcript_path.read_text(encoding="utf-8")

    # Load prompt
    prompt = load_prompt(args.prompt)

    # Set default model per provider
    default_models = {
        "ollama": "llama3.1",
        "claude": "claude-sonnet-4-20250514",
        "openai": "gpt-4o"
    }
    model = args.model or default_models[args.provider]

    # Generate report
    if args.provider == "ollama":
        result = generate_report_ollama(transcript, prompt, model)
    elif args.provider == "claude":
        result = generate_report_claude(transcript, prompt, model)
    else:  # openai
        result = generate_report_openai(transcript, prompt, model)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = transcript_path.parent / f"{transcript_path.stem}_report.md"

    # Write output
    output_path.write_text(result["content"], encoding="utf-8")

    print(f"\nReport saved to: {output_path}")
    print(f"Provider: {result['provider']}")
    print(f"Model: {result['model']}")

    if "usage" in result:
        print(f"Tokens used: {result['usage']}")

if __name__ == "__main__":
    main()
