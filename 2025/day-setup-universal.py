#!/usr/bin/env python3
"""
Advent of Code Setup Script - Universal Version

Handles both current AoC puzzles (if in season) and any past Advent of Code puzzles.
Provides intelligent defaults with manual override capabilities.
"""

import argparse
import os
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Optional, Tuple, List
import logging

try:
    from aocd import get_data, get_puzzle
    from dotenv import load_dotenv
    load_dotenv()
except ImportError as e:
    print(f"Error importing required packages: {e}")
    print("Please install: pip install aocd python-dotenv")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
DEFAULT_PARENT_DIR = "./src"
DEFAULT_FOLDER_PREFIX = "day_"
CURRENT_YEAR = datetime.now().year
CURRENT_MONTH = datetime.now().month
CURRENT_DAY = datetime.now().day

class AoCSetupError(Exception):
    """Custom exception for setup errors."""
    pass

class AoCDateError(AoCSetupError):
    """Exception for invalid AoC dates."""
    pass

def get_available_aoc_years() -> List[int]:
    """Get list of years when AoC was available."""
    # AoC started in 2015
    # Check if current year is available (may not have completed yet)
    current_year_available = CURRENT_YEAR if CURRENT_YEAR >= 2015 else 2015
    return list(range(2015, current_year_available + 1))

def get_seasonal_day_suggestion() -> Optional[int]:
    """
    Suggest a day based on current season.
    Returns None if not in AoC season.
    """
    if CURRENT_MONTH == 12 and 1 <= CURRENT_DAY <= 25:
        return CURRENT_DAY
    return None

def suggest_best_puzzle() -> Tuple[int, int, str]:
    """
    Suggest the best puzzle to work on based on current date.

    Returns:
        Tuple of (day, year, reason)
    """
    seasonal_day = get_seasonal_day_suggestion()

    if seasonal_day:
        # It's currently AoC season
        reason = f"Today is Day {seasonal_day} of AoC {CURRENT_YEAR}!"
        return seasonal_day, CURRENT_YEAR, reason
    elif CURRENT_MONTH == 12 and CURRENT_DAY > 25:
        # Past December 25th - suggest most recent completed year
        most_recent_year = CURRENT_YEAR if CURRENT_MONTH <= 12 else CURRENT_YEAR - 1
        if most_recent_year >= 2015:
            reason = f"AoC {CURRENT_YEAR} has ended, suggesting most recent: {most_recent_year}"
            return 1, most_recent_year, reason

    # Default to first puzzle ever (good for beginners or practice)
    reason = "Outside AoC season, suggesting the classic first puzzle"
    return 1, 2015, reason

def validate_puzzle_date(day: int, year: int) -> Tuple[bool, str, str]:
    """
    Validate if a puzzle date is valid and available.

    Args:
        day: Day of month (1-25)
        year: Year of puzzle

    Returns:
        Tuple of (is_valid, status_message, availability_message)
    """
    # Basic validation
    if not (1 <= day <= 25):
        return False, "Invalid day", "Day must be between 1 and 25"

    if year < 2015 or year > CURRENT_YEAR + 1:
        return False, "Invalid year", f"Year must be between 2015 and {CURRENT_YEAR + 1}"

    # Check if it's in the future
    puzzle_date = date(year, 12, day)
    today = date.today()

    if puzzle_date > today:
        days_ahead = (puzzle_date - today).days
        return False, "Future puzzle", f"Puzzle releases in {days_ahead} day{'s' if days_ahead != 1 else ''}"

    # Check if it's during current season but not yet released
    if (year == CURRENT_YEAR and
        CURRENT_MONTH == 12 and
        day > CURRENT_DAY):
        days_until = day - CURRENT_DAY
        return False, "Not yet released", f"Releases in {days_until} day{'s' if days_until != 1 else ''}"

    # Check year completion status
    if year == CURRENT_YEAR:
        if CURRENT_MONTH < 12:
            return True, "Available", "Historical data for current year"
        elif CURRENT_MONTH > 12:
            return True, "Available", "Completed AoC year"
        else:  # December
            if day <= CURRENT_DAY:
                return True, "Available", "Current AoC day" if day == CURRENT_DAY else "Historical day this year"
            else:
                return False, "Future", "Future AoC day"

    return True, "Available", "Historical AoC puzzle"

def fetch_puzzle_with_retry(day: int, year: int, max_retries: int = 3) -> Tuple[str, str, bool]:
    """
    Fetch puzzle data with retry logic.

    Args:
        day: Day of puzzle
        year: Year of puzzle
        max_retries: Maximum number of retry attempts

    Returns:
        Tuple of (input_data, puzzle_info, success)
    """
    is_valid, status, message = validate_puzzle_date(day, year)

    if not is_valid and status in ["Future puzzle", "Not yet released"]:
        return "", "", False

    last_error = None
    for attempt in range(max_retries):
        try:
            logger.info(f"Fetching puzzle data (attempt {attempt + 1}/{max_retries})...")

            # Use block=False to avoid hanging
            input_data = get_data(day=day, year=year, block=False)
            puzzle_info = get_puzzle(day=day, year=year)

            return input_data, str(puzzle_info), True

        except Exception as e:
            last_error = e
            logger.warning(f"Attempt {attempt + 1} failed: {e}")

            if attempt < max_retries - 1:
                import time
                time.sleep(2 ** attempt)  # Exponential backoff

    # All retries failed
    error_msg = f"Failed to fetch after {max_retries} attempts: {last_error}"
    logger.error(error_msg)

    # Check if it's an availability issue
    if "not available" in str(last_error).lower():
        return "", "", False

    raise AoCSetupError(error_msg)

def create_folder_structure(parent_dir: Path, folder_name: str) -> Path:
    """Create the folder structure for the puzzle."""
    try:
        folder_path = parent_dir / folder_name
        parent_dir.mkdir(parents=True, exist_ok=True)
        folder_path.mkdir(exist_ok=True)
        logger.info(f"Created folder structure: {folder_path}")
        return folder_path
    except Exception as e:
        raise AoCSetupError(f"Failed to create folders: {e}")

def create_puzzle_files(folder_path: Path, day: int, year: int,
                       input_data: str, puzzle_title: str) -> List[Path]:
    """Create template files for the puzzle."""
    files_created = []

    try:
        # Input file
        input_file = folder_path / "input.txt"
        with open(input_file, 'w') as f:
            f.write(input_data)
        files_created.append(input_file)

        # Test input file
        test_input_file = folder_path / "test-input.txt"
        with open(test_input_file, 'w') as f:
            f.write(f"# Test input for Day {day}, {year}\n# Add your test cases here\n")
        files_created.append(test_input_file)

        # Solution file
        solution_file = folder_path / "solution.py"
        solution_template = f'''#!/usr/bin/env python3
"""
Advent of Code Day {day}, {year}

Puzzle: {puzzle_title}
"""

def solve_part_1(data: str) -> int:
    """Solve part 1 of the puzzle."""
    # TODO: Implement solution
    lines = data.strip().split('\\n')
    # Your solution here
    return 0

def solve_part_2(data: str) -> int:
    """Solve part 2 of the puzzle."""
    # TODO: Implement solution
    lines = data.strip().split('\\n')
    # Your solution here
    return 0

def main():
    """Main execution function."""
    with open("input.txt", "r") as f:
        data = f.read().strip()

    result_1 = solve_part_1(data)
    result_2 = solve_part_2(data)

    print(f"Part 1: {{result_1}}")
    print(f"Part 2: {{result_2}}")

if __name__ == "__main__":
    main()
'''

        with open(solution_file, 'w') as f:
            f.write(solution_template)
        files_created.append(solution_file)

        # Make executable on Unix-like systems
        if os.name != 'nt':
            try:
                solution_file.chmod(0o755)
            except Exception as e:
                logger.warning(f"Could not make solution executable: {e}")

        return files_created

    except Exception as e:
        raise AoCSetupError(f"Failed to create files: {e}")

def interactive_puzzle_selection() -> Tuple[int, int]:
    """Interactive puzzle selection if no arguments provided."""
    print("\\n🎯 No specific puzzle requested. Let me suggest some options:")

    # Suggest best option
    suggested_day, suggested_year, reason = suggest_best_puzzle()
    print(f"\\n💡 RECOMMENDED: Day {suggested_day}, {year}")
    print(f"   Reason: {reason}")

    # Show available years
    available_years = get_available_aoc_years()
    print(f"\\n📚 Available years: {min(available_years)}-{max(available_years)}")

    # Interactive selection
    while True:
        try:
            print(f"\\nOptions:")
            print(f"1. Use recommendation (Day {suggested_day}, {suggested_year})")
            print(f"2. Choose specific day/year")
            print(f"3. See list of all available puzzles")
            print(f"4. Exit")

            choice = input("\\nSelect option (1-4): ").strip()

            if choice == "1":
                return suggested_day, suggested_year
            elif choice == "2":
                day = int(input("Day (1-25): "))
                year = int(input("Year: "))
                return day, year
            elif choice == "3":
                show_available_puzzles()
                continue
            elif choice == "4":
                print("Goodbye! 👋")
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")

        except (ValueError, KeyboardInterrupt):
            print("\\nGoodbye! 👋")
            sys.exit(0)

def show_available_puzzles():
    """Display available puzzles."""
    available_years = get_available_aoc_years()

    print("\\n📚 Available Advent of Code Puzzles:")
    print("=" * 50)

    for year in available_years:
        current_year_status = ""
        if year == CURRENT_YEAR:
            if CURRENT_MONTH == 12:
                if CURRENT_DAY <= 25:
                    current_year_status = f" (Day {CURRENT_DAY} available today!)"
                else:
                    current_year_status = " (Completed)"
            else:
                current_year_status = " (Not started yet)"

        print(f"{year}{current_year_status}")

        # Show a few examples for recent years
        if year >= 2020:
            examples = [1, 5, 10, 15, 20, 25]
            example_strs = []
            for day in examples:
                is_valid, status, message = validate_puzzle_date(day, year)
                if is_valid:
                    example_strs.append(str(day))
            if example_strs:
                print(f"   Available days: {', '.join(example_strs[:6])}...")

    print("=" * 50)

def setup_puzzle(day: int, year: int, folder_name: Optional[str] = None,
                parent_dir: str = DEFAULT_PARENT_DIR, force: bool = False) -> Path:
    """
    Complete puzzle setup process.

    Args:
        day: Day of puzzle
        year: Year of puzzle
        folder_name: Custom folder name
        parent_dir: Parent directory
        force: Force setup even if data unavailable

    Returns:
        Path to created folder
    """
    # Validate date first
    is_valid, status, message = validate_puzzle_date(day, year)

    if not is_valid and not force:
        raise AoCDateError(f"Cannot setup Day {day}, {year}: {message}")

    # Generate folder name if not provided
    if folder_name is None:
        folder_name = f"{DEFAULT_FOLDER_PREFIX}{day:02d}"

    print(f"\\n🎯 Setting up Day {day}, {year}")
    print(f"📁 Folder: {folder_name}")
    print(f"📊 Status: {status} - {message}")

    # Fetch puzzle data
    input_data, puzzle_info, success = fetch_puzzle_with_retry(day, year)

    if not success and not force:
        raise AoCSetupError(f"Puzzle data not available for Day {day}, {year}")

    if not success:
        print("⚠️  Puzzle data not available, creating template files only")
        input_data = "# Puzzle data not available\\n# This is a template file\\n"
        puzzle_info = f"Day {day}, {year} (Data unavailable)"

    # Display puzzle info
    print(f"\\n📋 Puzzle Information:")
    print("=" * 60)
    if puzzle_info:
        print(puzzle_info)
    else:
        print(f"Day {day}, {year} (No description available)")
    print("=" * 60)

    # Create folder structure
    parent_path = Path(parent_dir)
    folder_path = create_folder_structure(parent_path, folder_name)

    # Create files
    files_created = create_puzzle_files(folder_path, day, year, input_data, puzzle_info)

    # Summary
    print(f"\\n✅ Setup complete!")
    print(f"📁 Location: {folder_path}")
    print(f"📄 Files created ({len(files_created)}):")
    for file_path in files_created:
        size = file_path.stat().st_size
        print(f"   • {file_path.name} ({size:,} bytes)")

    return folder_path

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Setup Advent of Code puzzles (current or historical)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Smart Usage:
  • No args: Interactive mode with suggestions
  • --suggest: Use AI-recommended puzzle
  • --current: Setup current AoC day (if in season)
  • --past: Setup classic past puzzles
  • Manual: Specify exact day/year

Examples:
  python day-setup-universal.py                    # Interactive with suggestions
  python day-setup-universal.py --suggest          # Use recommended puzzle
  python day-setup-universal.py --current          # Current AoC day (if available)
  python day-setup-universal.py --day 1 --year 2020 # Specific historical puzzle
  python day-setup-universal.py --past             # Classic Day 1, 2015
  python day-setup-universal.py --list             # Show all available puzzles
        """
    )

    # Selection modes
    selection_group = parser.add_mutually_exclusive_group()
    selection_group.add_argument(
        "--suggest", action="store_true",
        help="Use AI-recommended puzzle based on current season"
    )
    selection_group.add_argument(
        "--current", action="store_true",
        help="Setup current AoC day (only works during December 1-25)"
    )
    selection_group.add_argument(
        "--past", action="store_true",
        help="Setup classic Day 1, 2015 (great for beginners)"
    )
    selection_group.add_argument(
        "--list", action="store_true",
        help="List all available puzzles and exit"
    )

    # Manual specification
    parser.add_argument("--day", type=int, help="Day of month (1-25)")
    parser.add_argument("--year", type=int, help="Year of puzzle")

    # Configuration
    parser.add_argument("--folder", type=str, help="Custom folder name")
    parser.add_argument("--parent-dir", type=str, default=DEFAULT_PARENT_DIR,
                       help=f"Parent directory (default: {DEFAULT_PARENT_DIR})")
    parser.add_argument("--force", action="store_true",
                       help="Force setup even if data unavailable")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Handle list option first
        if args.list:
            show_available_puzzles()
            return

        # Determine which puzzle to setup
        if args.current:
            seasonal_day = get_seasonal_day_suggestion()
            if seasonal_day is None:
                print("❌ --current only works during December 1-25")
                print(f"💡 Today is {datetime.now().strftime('%B %d, %Y')}")
                sys.exit(1)
            day, year = seasonal_day, CURRENT_YEAR
        elif args.past:
            day, year = 1, 2015
        elif args.suggest:
            day, year, reason = suggest_best_puzzle()
            print(f"💡 {reason}")
        elif args.day is not None and args.year is not None:
            day, year = args.day, args.year
        elif args.day is not None or args.year is not None:
            print("❌ Both --day and --year must be specified together")
            sys.exit(1)
        else:
            # Interactive mode
            day, year = interactive_puzzle_selection()

        # Setup the puzzle
        setup_puzzle(day, year, args.folder, args.parent_dir, args.force)

    except (AoCSetupError, AoCDateError) as e:
        print(f"❌ {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\\n❌ Setup interrupted by user")
        sys.exit(1)

if __name__ == "__main__":
    main()
