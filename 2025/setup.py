#!/usr/bin/env python3
"""
Advent of Code Setup Script

Clean, minimal setup for AoC puzzles with smart defaults.
"""

import argparse
import os
from datetime import datetime
from pathlib import Path

try:
    from aocd import get_data, get_puzzle
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Install dependencies: pip install aocd python-dotenv")
    exit(1)

def setup_day(day: int, year: int = None, folder: str = None):
    """Setup AoC day with minimal code."""
    year = year or datetime.now().year
    folder = folder or f"day_{day:02d}"
    
    # Fetch data
    try:
        data = get_data(day=day, year=year)
        puzzle = get_puzzle(day=day, year=year)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return
    
    # Create structure
    folder_path = Path("src") / folder
    folder_path.mkdir(parents=True, exist_ok=True)
    
    # Create files
    (folder_path / "input.txt").write_text(data)
    (folder_path / "test-input.txt").write_text("")
    (folder_path / "solution.py").write_text(f'''#!/usr/bin/env python3
"""Day {day}, {year}"""

def solve_part_1(data: str) -> int:
    lines = data.strip().split('\\n')
    return 0

def solve_part_2(data: str) -> int:
    lines = data.strip().split('\\n')
    return 0

if __name__ == "__main__":
    with open("input.txt") as f:
        data = f.read()
    
    print(f"Part 1: {{solve_part_1(data)}}")
    print(f"Part 2: {{solve_part_2(data)}}")
''')
    
    print(f"✅ Setup complete: {folder_path}")
    print(f"📋 {puzzle.title}")

def main():
    parser = argparse.ArgumentParser(description="Setup AoC day")
    parser.add_argument("day", type=int, help="Day (1-25)")
    parser.add_argument("--year", type=int, help="Year")
    parser.add_argument("--folder", help="Folder name")
    
    args = parser.parse_args()
    setup_day(args.day, args.year, args.folder)

if __name__ == "__main__":
    main()