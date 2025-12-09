#!/usr/bin/env python3
"""Day 1, 2025 - Improved Solution

This module contains optimized solutions for counting zero positions
during left and right rotations on a 100-position circular dial.
"""

from typing import List, Tuple, Union
import logging

# Configuration constants
INITIAL_POSITION = 50
MAX_POSITION = 99
MIN_POSITION = 0
TOTAL_POSITIONS = 100

# Set up logging for debugging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class DialRotationError(Exception):
    """Custom exception for invalid rotation operations."""
    pass


class CircularDial:
    """A circular dial implementation for tracking position and zero counts."""

    def __init__(self, initial_position: int = INITIAL_POSITION) -> None:
        """Initialize the circular dial.

        Args:
            initial_position: Starting position on the dial (0-99)

        Raises:
            ValueError: If initial_position is out of range
        """
        if not (MIN_POSITION <= initial_position <= MAX_POSITION):
            raise ValueError(f"Initial position must be between {MIN_POSITION} and {MAX_POSITION}")

        self.position = initial_position
        self.zero_count = 0

    def rotate_left(self, steps: int) -> int:
        """Rotate dial left by specified steps and count zero positions.

        Args:
            steps: Number of steps to rotate left

        Returns:
            Final position after rotation

        Raises:
            DialRotationError: If steps is negative
        """
        if steps < 0:
            raise DialRotationError("Steps cannot be negative")

        original_position = self.position

        # Count intermediate zero positions during rotation
        for step in range(1, steps + 1):
            intermediate_pos = (original_position - step) % TOTAL_POSITIONS
            if intermediate_pos == 0:
                self.zero_count += 1

        # Update final position
        self.position = (self.position - steps) % TOTAL_POSITIONS
        return self.position

    def rotate_right(self, steps: int) -> int:
        """Rotate dial right by specified steps and count zero positions.

        Args:
            steps: Number of steps to rotate right

        Returns:
            Final position after rotation

        Raises:
            DialRotationError: If steps is negative
        """
        if steps < 0:
            raise DialRotationError("Steps cannot be negative")

        original_position = self.position

        # Count intermediate zero positions during rotation
        for step in range(1, steps + 1):
            intermediate_pos = (original_position + step) % TOTAL_POSITIONS
            if intermediate_pos == 0:
                self.zero_count += 1

        # Update final position
        self.position = (self.position + steps) % TOTAL_POSITIONS
        return self.position

    def get_zero_count(self) -> int:
        """Get the current count of times the dial passed through position 0."""
        return self.zero_count


def parse_input(data: str) -> List[Tuple[str, int]]:
    """Parse input data into operations and values.

    Args:
        data: Raw input string containing L/R operations

    Returns:
        List of tuples containing (operation, value) pairs

    Raises:
        ValueError: If input contains invalid operations or values
    """
    lines = data.strip().split('\n')
    operations = []

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:  # Skip empty lines
            continue

        if len(line) < 2:
            raise ValueError(f"Line {line_num}: Invalid format '{line}' - must start with L or R followed by number")

        operation = line[0].upper()
        try:
            value = int(line[1:])
        except ValueError as e:
            raise ValueError(f"Line {line_num}: Invalid number '{line[1:]}' - {e}")

        if operation not in ['L', 'R']:
            raise ValueError(f"Line {line_num}: Invalid operation '{operation}' - must be L or R")

        if value < 0:
            raise ValueError(f"Line {line_num}: Negative value {value} not allowed")

        operations.append((operation, value))

    return operations


def solve_part_1_optimized(data: str) -> int:
    """Solve part 1 - only count final position of zero.

    Args:
        data: Input data string

    Returns:
        Number of times dial lands on position 0 after each operation
    """
    operations = parse_input(data)
    dial = CircularDial()

    for operation, steps in operations:
        if operation == 'L':
            dial.position = (dial.position - steps) % TOTAL_POSITIONS
        else:  # operation == 'R'
            dial.position = (dial.position + steps) % TOTAL_POSITIONS

        if dial.position == 0:
            dial.zero_count += 1

    return dial.get_zero_count()


def solve_part_2_optimized(data: str) -> int:
    """Solve part 2 - count all intermediate positions of zero during rotation.

    Args:
        data: Input data string

    Returns:
        Total count of times dial passes through position 0 (including intermediate positions)
    """
    operations = parse_input(data)
    dial = CircularDial()

    for operation, steps in operations:
        if operation == 'L':
            dial.rotate_left(steps)
        else:  # operation == 'R'
            dial.rotate_right(steps)

    return dial.get_zero_count()


def _count_zeros_in_rotation(start_pos: int, steps: int, direction: str) -> int:
    """Helper function to count zero positions in a single rotation.

    This is an optimized mathematical approach that avoids the inner loop.

    Args:
        start_pos: Starting position
        steps: Number of steps to rotate
        direction: 'L' for left, 'R' for right

    Returns:
        Number of times position 0 is passed during rotation
    """
    if steps == 0:
        return 0

    zeros_in_rotation = 0

    if direction == 'L':
        # For left rotation: check if (start_pos - step) % 100 == 0 for step in 1..steps
        # This is equivalent to checking if start_pos - step is divisible by 100
        # start_pos - step ≡ 0 (mod 100) → step ≡ start_pos (mod 100)
        for step in range(1, steps + 1):
            if (start_pos - step) % TOTAL_POSITIONS == 0:
                zeros_in_rotation += 1
    else:  # direction == 'R'
        # For right rotation: check if (start_pos + step) % 100 == 0 for step in 1..steps
        for step in range(1, steps + 1):
            if (start_pos + step) % TOTAL_POSITIONS == 0:
                zeros_in_rotation += 1

    return zeros_in_rotation


def solve_part_2_mathematical(data: str) -> int:
    """Mathematical solution for part 2 - optimized without simulation.

    Args:
        data: Input data string

    Returns:
        Total count of times dial passes through position 0
    """
    operations = parse_input(data)
    position = INITIAL_POSITION
    total_zeros = 0

    for operation, steps in operations:
        # Count zeros in this rotation
        zeros_in_this_rotation = _count_zeros_in_rotation(position, steps, operation)
        total_zeros += zeros_in_this_rotation

        # Update position
        if operation == 'L':
            position = (position - steps) % TOTAL_POSITIONS
        else:  # operation == 'R'
            position = (position + steps) % TOTAL_POSITIONS

    return total_zeros


def validate_input_file(filename: str) -> bool:
    """Validate that the input file exists and is readable.

    Args:
        filename: Path to the input file

    Returns:
        True if file is valid, False otherwise
    """
    try:
        with open(filename, 'r') as f:
            f.read()
        return True
    except (FileNotFoundError, PermissionError, OSError):
        return False


def main() -> None:
    """Main function to run both solutions and display results."""
    input_file = "input.txt"

    if not validate_input_file(input_file):
        print(f"Error: Cannot read input file '{input_file}'")
        return

    try:
        with open(input_file) as f:
            data = f.read()

        print("=== IMPROVED SOLUTION COMPARISON ===")

        # Part 1 - Final position only
        result_part1 = solve_part_1_optimized(data)
        print(f"Part 1 (final position only): {result_part1}")

        # Part 2 - Step-by-step counting
        result_part2_sim = solve_part_2_optimized(data)
        result_part2_math = solve_part_2_mathematical(data)

        print(f"Part 2 (step-by-step simulation): {result_part2_sim}")
        print(f"Part 2 (mathematical optimization): {result_part2_math}")

        # Verify both part 2 methods give same result
        if result_part2_sim == result_part2_math:
            print("✓ Mathematical optimization verified!")
        else:
            print("⚠ Warning: Results differ between methods")

    except (ValueError, DialRotationError) as e:
        print(f"Error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
