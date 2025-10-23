#!/usr/bin/env python3
"""
StoryForge - Simple story generation script
"""

import subprocess
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_story.py <prompt_file>")
        print("Example: python run_story.py prompts/example_fantasy.txt")
        return
    
    prompt_file = sys.argv[1]
    if not Path(prompt_file).exists():
        print(f"Error: Prompt file '{prompt_file}' not found")
        return
    
    print(f"🚀 Generating story with StoryForge...")
    print(f"📝 Using prompt: {prompt_file}")
    
    # Run with local models and no revisions for speed
    cmd = [
        "python", "Write.py",
        "-Prompt", prompt_file,
        "-NoChapterRevision",
        "-NoScrubChapters"
    ]
    
    subprocess.run(cmd)

if __name__ == "__main__":
    main()