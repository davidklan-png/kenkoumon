#!/usr/bin/env python3
"""
Generate mock audio recordings from JSON transcripts.
Uses gTTS for Japanese text-to-speech.
"""

import json
import os
import sys
from pathlib import Path
from gtts import gTTS
import time

# Directories
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
MOCK_DIR = PROJECT_ROOT / "backend" / "tests" / "mock_recordings"
OUTPUT_DIR = PROJECT_ROOT / "backend" / "tests" / "mock_audio"

def load_scenario(scenario_file: Path) -> dict:
    """Load a scenario JSON file."""
    with open(scenario_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_audio_files(scenario: dict, output_dir: Path):
    """Generate individual audio files for each turn, then combine info."""
    scenario_id = scenario['id']
    scenario_name = scenario['scenario']
    
    # Create subdirectory for this scenario
    scenario_dir = output_dir / f"{scenario_id}_{scenario_name}"
    scenario_dir.mkdir(parents=True, exist_ok=True)
    
    files_info = []
    
    for i, turn in enumerate(scenario['transcript']):
        speaker = turn['speaker']
        text = turn['text']
        
        # Generate filename
        filename = f"{i:03d}_{speaker}.mp3"
        filepath = scenario_dir / filename
        
        # Generate speech
        print(f"  [{i+1}/{len(scenario['transcript'])}] {speaker}: {text[:40]}...")
        tts = gTTS(text=text, lang='ja', slow=False)
        tts.save(str(filepath))
        
        files_info.append({
            'index': i,
            'speaker': speaker,
            'text': text,
            'file': filename,
            'timestamp_start': turn.get('timestamp_start', 0),
            'timestamp_end': turn.get('timestamp_end', 0)
        })
        
        # Small delay to avoid rate limiting
        time.sleep(0.3)
    
    # Save metadata
    metadata = {
        'scenario_id': scenario_id,
        'scenario': scenario_name,
        'title': scenario['title'],
        'participants': scenario['participants'],
        'total_turns': len(files_info),
        'files': files_info
    }
    
    metadata_file = scenario_dir / 'metadata.json'
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    return scenario_dir, len(files_info)

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate mock audio from JSON transcripts')
    parser.add_argument('--scenario', '-s', help='Specific scenario ID (e.g., mock_001)')
    parser.add_argument('--all', '-a', action='store_true', help='Generate all scenarios')
    parser.add_argument('--output', '-o', default=str(OUTPUT_DIR), help='Output directory')
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find scenarios to process
    if args.scenario:
        scenario_files = list(MOCK_DIR.glob(f"scenario_{args.scenario.split('_')[1]}_*.json"))
    else:
        scenario_files = sorted(MOCK_DIR.glob("scenario_*.json"))
    
    if not scenario_files:
        print("No scenarios found!")
        sys.exit(1)
    
    print(f"Found {len(scenario_files)} scenarios to process\n")
    
    total_files = 0
    for scenario_file in scenario_files:
        print(f"Processing: {scenario_file.name}")
        scenario = load_scenario(scenario_file)
        
        scenario_dir, num_files = generate_audio_files(scenario, output_dir)
        total_files += num_files
        
        print(f"  ✓ Generated {num_files} audio files in {scenario_dir.name}\n")
    
    print(f"Done! {total_files} audio files in {output_dir}")

if __name__ == '__main__':
    main()
