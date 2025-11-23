#!/usr/bin/env python3
"""
Advent of Code Day Setup Script - Auto-detecting version

This script automatically detects the current date and provides smart defaults
for Advent of Code setup, with intelligent handling of the seasonal nature of AoC.
"""

import argparse
import os
import sys
from datetime import datetime, date
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
CURRENT_YEAR = datetime.now().year
CURRENT_MONTH = datetime.now().month
CURRENT_DAY = datetime.now().day

DEFAULT_YEAR = CURRENT_YEAR  # Auto-detect current year
DEFAULT_PARENT_DIR = "./src"
DEFAULT_FOLDER_PREFIX = "day_"

# Advent of Code season detection
def is_aoc_season(target_year: int = None) -> bool:
    """
    Check if it's currently Advent of Code season.

    Args:
        target_year: Year to check (defaults to current year)

    Returns:
        True if it's December 1-25 of the target year
    """
    if target_year is None:
        target_year = CURRENT_YEAR

    today = date.today()
    # Check if it's December 1-25 of the target year
    return (today.year == target_year and
            today.month == 12 and
            1 <= today.day <= 25)

def get_smart_defaults() -> Tuple[int, int, Optional[str]]:
    """
    Get intelligent defaults based on current date.

    Returns:
        Tuple of (day, year, folder_name)
    """
    if is_aoc_season():
        # It's Advent of Code season - use current day
        smart_day = min(CURRENT_DAY, 25)  # Cap at day 25
        smart_year = CURRENT_YEAR
        folder_name = f"{DEFAULT_FOLDER_PREFIX}{smart_day:02d}"
        logger.info(f"Detected AoC season - using day {smart_day}, year {smart_year}")
    else:
        # Not AoC season - use reasonable defaults
        if CURRENT_MONTH > 12:
            # Past December, suggest next year's AoC
            smart_day = 1
            smart_year = CURRENT_YEAR + 1
            folder_name = f"{DEFAULT_FOLDER_PREFIX}{smart_day:02d}"
            logger.info(f"Past AoC season - suggesting day {smart_day}, year {smart_year}")
        else:
            # Before December, suggest this year's AoC (if available)
            if CURRENT_YEAR >= 2015:  # AoC started in 2015
                smart_day = 1
                smart_year = CURRENT_YEAR
                folder_name = f"{DEFAULT_FOLDER_PREFIX}{smart_day:02d}"
                logger.info(f"Pre-season - using day {smart_day}, year {smart_year}")
            else:
                smart_day = 1
                smart_year = 2015  # First AoC year
                folder_name = f"{DEFAULT_FOLDER_PREFIX}{smart_day:02d}"
                logger.info(f"Using first AoC - day {smart_day}, year {smart_year}")

    return smart_day, smart_year, folder_name

def validate_date_for_aoc(day: int, year: int) -> Tuple[bool, str]:
    """
    Validate if the given date is valid for Advent of Code.

    Args:
        day: Day of the month
        year: Year

    Returns:
        Tuple of (is_valid, message)
    """
    # Basic validation
    if not (1 <= day <= 25):
        return False, f"Day must be between 1 and 25, got {day}"

    if year < 2015:
        return False, f"Year must be 2015 or later (AoC started in 2015), got {year}"

    if year > CURRENT_YEAR + 1:
        return False, f"Year too far in the future: {year} (current: {CURRENT_YEAR})"

    # Check if date is in the future
    target_date = date(year, 12, day)
    today = date.today()

    if target_date > today:
        return False, f"Date {target_date} is in the future (today: {today})"

    # If it's AoC season, check if the day is available
    if year == CURRENT_YEAR and CURRENT_MONTH == 12:
        if day > CURRENT_DAY:
            return False, f"Day {day} of December {year} hasn't been released yet (today: {CURRENT_DAY})"

    return True, "Date is valid for AoC"

def fetch_puzzle_data_with_seasonal_check(day: int, year: int) -> Tuple[str, str, bool]:
    """
    Fetch puzzle data with seasonal awareness.

    Args:
        day: Day of the month
        year: Year of the puzzle

    Returns:
        Tuple of (input_data, puzzle_info, is_available)
    """
    # Check if this is a future date
    validation_ok, validation_msg = validate_date_for_aoc(day, year)
    if not validation_ok:
        raise ValueError(validation_msg)

    try:
        # Attempt to fetch the data
        logger.info(f"Attempting to fetch puzzle data for day {day}, year {year}")

        aoc_data = get_data(day=day, year=year, block=False)
        aoc_puzzle = get_puzzle(day=day, year=year)

        return aoc_data, str(aoc_puzzle), True

    except Exception as e:
        # Check if it's a data not available error
        error_msg = str(e).lower()
        if any(keyword in error_msg for keyword in ['not available', 'not released', 'blocked']):
            logger.warning(f"Puzzle data not yet available: {e}")
            return "", "", False
        else:
            # Re-raise other errors
            raise

def create_seasonal_setup_message(day: int, year: int, is_available: bool) -> str:
    """
    Create an informative message based on the seasonal context.

    Args:
        day: Day number
        year: Year
        is_available: Whether puzzle data is available

    Returns:
        Informative message string
    """
    today = date.today()

    if is_available:
        if year == CURRENT_YEAR and CURRENT_MONTH == 12 and day == CURRENT_DAY:
            return f"🎄 Setting up TODAY'S Advent of Code puzzle! (Day {day}, {year})"
        elif year == CURRENT_YEAR and CURRENT_MONTH == 12:
            return f"🎄 Setting up Day {day} of {year} Advent of Code"
        else:
            return f"📚 Setting up past Advent of Code puzzle (Day {day}, {year})"
    else:
        if year == CURRENT_YEAR and CURRENT_MONTH == 12 and day > CURRENT_DAY:
            days_until = day - CURRENT_DAY
            return f"⏰ Day {day} of {year} will be available in {days_until} day{'s' if days_until != 1 else ''}"
        elif year > CURRENT_YEAR or (year == CURRENT_YEAR and CURRENT_MONTH > 12):
            return f"⏰ Setting up future Advent of Code (Day {day}, {year})"
        else:
            return f"⏰ Day {day} of {year} is not yet available"

def main():
    """Main entry point with enhanced seasonal awareness."""
    parser = argparse.ArgumentParser(
        description="Setup script for Advent of Code with seasonal intelligence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Smart defaults:
  - If it's December 1-25: Uses the current day
  - If it's before December: Suggests Day 1 of current year
  - If it's after December: Suggests Day 1 of next year

Examples:
  python day-setup-auto.py                           # Auto-detect best day
  python day-setup-auto.py --day 8                  # Use Day 8 of current year
  python day-setup-auto.py --day 1 --year 2025      # Use specific date
  python day-setup-auto.py --force --day 25         # Force setup even if unavailable
        """
    )

    parser.add_argument(
        "--day",
        type=int,
        help="Day of the month (1-25). If not specified, auto-detects based on season."
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
        help="Custom folder name (auto-generated if not specified)"
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

    parser.add_argument(
        "--force",
        action="store_true",
        help="Force setup even if puzzle data is not yet available"
    )

    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check if puzzle data is available, don't create files"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Determine day and year
        if args.day is not None:
            day = args.day
            year = args.year
            folder_name = args.folder or f"{DEFAULT_FOLDER_PREFIX}{day:02d}"
        else:
            day, year, folder_name = get_smart_defaults()
            logger.info(f"Auto-detected: Day {day}, Year {year}, Folder: {folder_name}")

        # Show current date context
        today = date.today()
        print(f"📅 Today: {today.strftime('%A, %B %d, %Y')}")
        print(f"🎯 Target: Day {day}, Year {year}")

        # Check availability
        validation_ok, validation_msg = validate_date_for_aoc(day, year)
        if not validation_ok:
            print(f"❌ {validation_msg}")
            if not args.force:
                print("💡 Use --force to override validation")
                sys.exit(1)

        # Try to fetch data
        try:
            input_data, puzzle_info, is_available = fetch_puzzle_data_with_seasonal_check(day, year)
        except Exception as e:
            print(f"❌ Failed to fetch puzzle data: {e}")
            if not args.force:
                print("💡 Use --force to continue without puzzle data")
                sys.exit(1)
            else:
                input_data, puzzle_info, is_available = "", "", False

        # Create informative message
        setup_message = create_seasonal_setup_message(day, year, is_available)
        print(f"\n{setup_message}")

        if not is_available and not args.force:
            print("💡 Use --force to create template files without puzzle data")
            sys.exit(0)

        if args.check_only:
            print("✅ Data availability check complete")
            sys.exit(0)

        # Display puzzle info if available
        if is_available and puzzle_info:
            print(f"\n📋 Puzzle Information:")
            print("=" * 50)
            print(puzzle_info)
            print("=" * 50)

        # For now, show what would be created (since we don't have the full setup logic here)
        parent_path = Path(args.parent_dir)
        folder_path = parent_path / folder_name

        print(f"\n📁 Would create folder: {folder_path}")
        print(f"📄 Would create files:")
        for file_type in ["input.txt", "test-input.txt", "solution.py"]:
            print(f"   • {file_type}")

        if not args.force and not is_available:
            print("\n💡 Use --force to create files without puzzle data")

    except KeyboardInterrupt:
        print("\n❌ Setup interrupted by user")
        sys.exit(1)

if __name__ == "__main__":
    main()
