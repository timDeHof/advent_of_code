#!/usr/bin/env python3
"""
Advent of Code Day Setup Script

This script automates the setup process for a new Advent of Code day by:
- Fetching puzzle data from the AoC API
- Creating the necessary folder structure
- Generating template files for input, test input, and solution

Usage:
    python day-setup-improved.py --day 8 --year 2024 --folder day_08
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional, Tuple
import logging

try:
    from aocd import get_data, get_puzzle
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Error importing required packages: {e}")
    print("Please install required packages: pip install aocd python-dotenv")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration constants
DEFAULT_YEAR = 2024
DEFAULT_PARENT_DIR = "./src"
DEFAULT_FOLDER_PREFIX = "day_"
TEMPLATE_FILES = {
    "input.txt": "",  # Will be populated with AoC data
    "test-input.txt": "# Add test cases here\n",
    "solution.py": '''#!/usr/bin/env python3
"""
Advent of Code Day {day} Solution

Problem: {problem_title}
"""

def solve_part_1(data: str) -> int:
    """Solve part 1 of the puzzle."""
    # TODO: Implement solution
    return 0

def solve_part_2(data: str) -> int:
    """Solve part 2 of the puzzle."""
    # TODO: Implement solution
    return 0

def main():
    """Main execution function."""
    # Load input data
    with open("input.txt", "r") as f:
        data = f.read().strip()

    # Solve parts
    result_1 = solve_part_1(data)
    result_2 = solve_part_2(data)

    print(f"Part 1: {{result_1}}")
    print(f"Part 2: {{result_2}}")

if __name__ == "__main__":
    main()
'''
}


class AoCSetupError(Exception):
    """Custom exception for AoC setup errors."""
    pass


def load_environment() -> bool:
    """Load environment variables and validate API access."""
    try:
        load_dotenv()
        # Check if AOCD_TOKEN is available (aocd will handle auth internally)
        logger.info("Environment loaded successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to load environment: {e}")
        return False


def fetch_puzzle_data(day: int, year: int, use_cache: bool = True) -> Tuple[str, str]:
    """
    Fetch puzzle data from AoC API with error handling.

    Args:
        day: Day of the month (1-25)
        year: Year of the puzzle
        use_cache: Whether to use cached data if available

    Returns:
        Tuple of (input_data, puzzle_info)

    Raises:
        AoCSetupError: If data fetching fails
    """
    try:
        logger.info(f"Fetching puzzle data for day {day}, year {year}")

        # Validate inputs
        if not (1 <= day <= 25):
            raise ValueError(f"Day must be between 1 and 25, got {day}")
        if year < 2015:  # AoC started in 2015
            raise ValueError(f"Year must be 2015 or later, got {year}")

        # Fetch data with timeout handling
        aoc_data = get_data(day=day, year=year, block=False)
        aoc_puzzle = get_puzzle(day=day, year=year)

        logger.info("Successfully fetched puzzle data")
        return aoc_data, str(aoc_puzzle)

    except Exception as e:
        error_msg = f"Failed to fetch puzzle data: {e}"
        logger.error(error_msg)
        raise AoCSetupError(error_msg) from e


def create_folder_structure(parent_dir: Path, folder_name: str) -> Path:
    """
    Create the folder structure for the AoC day.

    Args:
        parent_dir: Parent directory path
        folder_name: Name of the day folder

    Returns:
        Path to the created folder

    Raises:
        AoCSetupError: If folder creation fails
    """
    try:
        folder_path = parent_dir / folder_name

        # Ensure parent directory exists
        parent_dir.mkdir(parents=True, exist_ok=True)

        # Create the day folder
        folder_path.mkdir(exist_ok=True)

        logger.info(f"Created folder structure at {folder_path}")
        return folder_path

    except PermissionError as e:
        error_msg = f"Permission denied creating folder {folder_path}: {e}"
        logger.error(error_msg)
        raise AoCSetupError(error_msg) from e
    except Exception as e:
        error_msg = f"Failed to create folder structure: {e}"
        logger.error(error_msg)
        raise AoCSetupError(error_msg) from e


def create_template_files(folder_path: Path, day: int, year: int,
                         input_data: str, puzzle_title: str) -> None:
    """
    Create template files in the day folder.

    Args:
        folder_path: Path to the day folder
        day: Day number for template substitution
        year: Year for template substitution
        input_data: Raw input data from AoC
        puzzle_title: Title of the puzzle for template

    Raises:
        AoCSetupError: If file creation fails
    """
    try:
        files_created = []

        # Create input file with AoC data
        input_file = folder_path / "input.txt"
        with open(input_file, 'w') as f:
            f.write(input_data)
        files_created.append(input_file)

        # Create test input file
        test_input_file = folder_path / "test-input.txt"
        with open(test_input_file, 'w') as f:
            f.write(TEMPLATE_FILES["test-input.txt"])
        files_created.append(test_input_file)

        # Create solution file with template
        solution_file = folder_path / "solution.py"
        solution_content = TEMPLATE_FILES["solution.py"].format(
            day=day,
            problem_title=puzzle_title
        )
        with open(solution_file, 'w') as f:
            f.write(solution_content)
        files_created.append(solution_file)

        logger.info(f"Created {len(files_created)} template files")

        # Make solution file executable (Unix-like systems)
        if os.name != 'nt':  # Not Windows
            try:
                solution_file.chmod(0o755)
            except Exception as e:
                logger.warning(f"Could not make solution file executable: {e}")

    except Exception as e:
        error_msg = f"Failed to create template files: {e}"
        logger.error(error_msg)
        raise AoCSetupError(error_msg) from e


def setup_day(day: int, year: int, folder_name: Optional[str] = None,
              parent_dir: str = DEFAULT_PARENT_DIR, verbose: bool = False) -> Path:
    """
    Complete setup process for an Advent of Code day.

    Args:
        day: Day of the month (1-25)
        year: Year of the puzzle
        folder_name: Name of the day folder (auto-generated if None)
        parent_dir: Parent directory for day folders
        verbose: Enable verbose logging

    Returns:
        Path to the created day folder

    Raises:
        AoCSetupError: If setup process fails
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Generate folder name if not provided
        if folder_name is None:
            folder_name = f"{DEFAULT_FOLDER_PREFIX}{day:02d}"

        # Convert paths
        parent_path = Path(parent_dir)

        logger.info(f"Starting AoC day setup for day {day}, year {year}")
        logger.info(f"Folder: {folder_name}, Parent dir: {parent_dir}")

        # Load environment and validate access
        if not load_environment():
            raise AoCSetupError("Failed to load environment")

        # Fetch puzzle data
        input_data, puzzle_info = fetch_puzzle_data(day, year)

        # Display puzzle information
        print(f"\nPuzzle for Day {day}, {year}:")
        print("=" * 50)
        print(puzzle_info)
        print("=" * 50)

        # Create folder structure
        folder_path = create_folder_structure(parent_path, folder_name)

        # Extract puzzle title for template
        # Try to get title from puzzle info (format may vary)
        puzzle_title = f"Day {day} - {year}"
        if "---" in puzzle_info:
            lines = puzzle_info.split('\n')
            for line in lines:
                if line.strip() and not line.startswith('---'):
                    puzzle_title = line.strip()
                    break

        # Create template files
        create_template_files(folder_path, day, year, input_data, puzzle_title)

        # Summary
        print(f"\n✅ Setup complete!")
        print(f"📁 Folder: {folder_path}")
        print(f"📄 Files created:")
        for file_type in ["input.txt", "test-input.txt", "solution.py"]:
            file_path = folder_path / file_type
            if file_path.exists():
                size = file_path.stat().st_size
                print(f"   • {file_type} ({size} bytes)")

        return folder_path

    except Exception as e:
        error_msg = f"Setup failed: {e}"
        logger.error(error_msg)
        raise AoCSetupError(error_msg) from e


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Setup script for Advent of Code daily challenges",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python day-setup-improved.py --day 8 --year 2024
  python day-setup-improved.py --day 1 --year 2023 --folder day_01
  python day-setup-improved.py --day 25 --verbose
        """
    )

    parser.add_argument(
        "--day",
        type=int,
        required=True,
        help="Day of the month (1-25)"
    )

    parser.add_argument(
        "--year",
        type=int,
        default=DEFAULT_YEAR,
        help=f"Year of the puzzle (default: {DEFAULT_YEAR})"
    )

    parser.add_argument(
        "--folder",
        type=str,
        help="Custom folder name (default: day_XX where XX is day number)"
    )

    parser.add_argument(
        "--parent-dir",
        type=str,
        default=DEFAULT_PARENT_DIR,
        help=f"Parent directory for day folders (default: {DEFAULT_PARENT_DIR})"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    try:
        setup_day(
            day=args.day,
            year=args.year,
            folder_name=args.folder,
            parent_dir=args.parent_dir,
            verbose=args.verbose
        )
    except AoCSetupError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Setup interrupted by user")
        sys.exit(1)


if __name__ == "__main__":
    main()
