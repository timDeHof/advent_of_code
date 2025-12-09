#!/usr/bin/env python3
"""Day 2, 2025 - Improved Solution"""

import logging
from typing import Generator, List, Tuple
from dataclasses import dataclass


# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Range:
    """Represents a range of IDs with start and end values."""
    start: int
    end: int

    def __post_init__(self):
        """Validate range values after initialization."""
        if self.start > self.end:
            raise ValueError(f"Start value ({self.start}) cannot be greater than end value ({self.end})")
        if self.start < 0:
            raise ValueError(f"Start value ({self.start}) cannot be negative")

    def contains(self, value: int) -> bool:
        """Check if a value is within this range."""
        return self.start <= value <= self.end

    @classmethod
    def from_string(cls, range_str: str) -> 'Range':
        """Create a Range object from a string in format 'start-end'."""
        try:
            start_str, end_str = range_str.strip().split('-', 1)
            start = int(start_str)
            end = int(end_str)
            return cls(start, end)
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid range format '{range_str}'. Expected format: 'start-end'") from e


class InvalidIDDetector:
    """Class for detecting invalid IDs based on repetitive patterns."""

    @staticmethod
    def is_invalid_double_repetition(number: int) -> bool:
        """
        Check if a number is invalid due to exactly two repetitions of a substring.

        Args:
            number: The integer to check

        Returns:
            True if the number consists of exactly two repetitions of a substring

        Examples:
            55 -> True (5 repeated twice)
            6464 -> True (64 repeated twice)
            123123 -> True (123 repeated twice)
            123 -> False (not exactly two repetitions)
            1234 -> False (not repetitive)
        """
        str_num = str(number)
        length = len(str_num)

        # Must be even length for exact double repetition
        if length % 2 != 0:
            return False

        half_length = length // 2
        first_half = str_num[:half_length]
        second_half = str_num[half_length:]

        return first_half == second_half

    @staticmethod
    def is_invalid_multiple_repetition(number: int) -> bool:
        """
        Check if a number is invalid due to multiple repetitions of a substring.

        Args:
            number: The integer to check

        Returns:
            True if the number consists of 2 or more repetitions of a substring

        Examples:
            55 -> True (5 repeated twice)
            123123 -> True (123 repeated twice)
            123123123 -> True (123 repeated three times)
            1111111 -> True (1 repeated seven times)
            1234 -> False (not repetitive)
            123 -> False (not repetitive)
        """
        str_num = str(number)
        length = len(str_num)

        # Check all possible substring lengths that divide the total length
        for substring_length in range(1, length // 2 + 1):
            if length % substring_length == 0:
                substring = str_num[:substring_length]
                repetitions = length // substring_length

                # Check if the entire string is made of this substring repeated
                if substring * repetitions == str_num and repetitions >= 2:
                    return True

        return False


class DataProcessor:
    """Handles parsing and processing of input data."""

    @staticmethod
    def parse_ranges(data: str) -> List[Range]:
        """
        Parse input data into a list of Range objects.

        Args:
            data: Input string containing ranges separated by commas

        Returns:
            List of Range objects

        Raises:
            ValueError: If input format is invalid
        """
        if not data.strip():
            raise ValueError("Input data cannot be empty")

        ranges = []
        range_strings = data.strip().split(',')

        for i, range_str in enumerate(range_strings):
            try:
                range_obj = Range.from_string(range_str)
                ranges.append(range_obj)
            except ValueError as e:
                raise ValueError(f"Invalid range at position {i + 1}: {range_str}") from e

        return ranges

    @staticmethod
    def generate_numbers_in_range(range_obj: Range) -> Generator[int, None, None]:
        """
        Generate all numbers within a given range.

        Args:
            range_obj: Range object defining the boundaries

        Yields:
            Integer values within the range
        """
        for number in range(range_obj.start, range_obj.end + 1):
            yield number


class Solution:
    """Main solution class for Day 2, 2025."""

    def __init__(self):
        self.detector = InvalidIDDetector()
        self.processor = DataProcessor()

    def solve_part_1(self, data: str) -> int:
        """
        Solve part 1 of the problem.

        Finds all invalid IDs that consist of exactly two repetitions of a substring.

        Args:
            data: Input string containing ranges separated by commas

        Returns:
            Sum of all invalid IDs

        Raises:
            ValueError: If input format is invalid
        """
        try:
            ranges = self.processor.parse_ranges(data)
        except ValueError as e:
            logger.error(f"Failed to parse input data: {e}")
            raise

        invalid_ids = []

        for range_obj in ranges:
            try:
                for number in self.processor.generate_numbers_in_range(range_obj):
                    if self.detector.is_invalid_double_repetition(number):
                        invalid_ids.append(number)
            except Exception as e:
                logger.error(f"Error processing range {range_obj}: {e}")
                continue

        return sum(invalid_ids)

    def solve_part_2(self, data: str) -> int:
        """
        Solve part 2 of the problem.

        Finds all invalid IDs that consist of multiple repetitions (2 or more) of a substring.

        Args:
            data: Input string containing ranges separated by commas

        Returns:
            Sum of all invalid IDs

        Raises:
            ValueError: If input format is invalid
        """
        try:
            ranges = self.processor.parse_ranges(data)
        except ValueError as e:
            logger.error(f"Failed to parse input data: {e}")
            raise

        invalid_ids = []

        for range_obj in ranges:
            try:
                for number in self.processor.generate_numbers_in_range(range_obj):
                    if self.detector.is_invalid_multiple_repetition(number):
                        invalid_ids.append(number)
            except Exception as e:
                logger.error(f"Error processing range {range_obj}: {e}")
                continue

        return sum(invalid_ids)


def load_input_file(filepath: str = "input.txt") -> str:
    """
    Load input data from file.

    Args:
        filepath: Path to the input file

    Returns:
        Contents of the file as a string

    Raises:
        FileNotFoundError: If the file doesn't exist
        IOError: If there's an error reading the file
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file '{filepath}' not found")
    except IOError as e:
        raise IOError(f"Error reading file '{filepath}': {e}")


def main():
    """Main function to execute the solution."""
    try:
        # Load input data
        data = load_input_file()

        # Create solution instance
        solution = Solution()

        # Solve both parts
        part_1_result = solution.solve_part_1(data)
        part_2_result = solution.solve_part_2(data)

        # Print results
        print(f"Part 1: {part_1_result}")
        print(f"Part 2: {part_2_result}")

    except (FileNotFoundError, IOError, ValueError) as e:
        logger.error(f"Failed to execute solution: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
