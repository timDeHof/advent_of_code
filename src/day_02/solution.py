#!/usr/bin/env python3
"""Day 2, 2025 - Refactored Solution"""

def is_double_repetition(number: int) -> bool:
    """
    Check if a number consists of exactly two repetitions of a substring.

    Args:
        number: The integer to check

    Returns:
        True if the number has the pattern ABCABC, False otherwise

    Examples:
        55 -> True (5 twice)
        6464 -> True (64 twice)
        123123 -> True (123 twice)
        123 -> False (odd length)
        1234 -> False (halves don't match)
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


def is_multiple_repetition(number: int) -> bool:
    """
    Check if a number consists of multiple repetitions of a substring (2+ times).

    Args:
        number: The integer to check

    Returns:
        True if the number has repeated pattern (ABCABC, ABCABCABC, etc.), False otherwise

    Examples:
        55 -> True (5 twice)
        123123 -> True (123 twice)
        123123123 -> True (123 three times)
        1111111 -> True (1 seven times)
        123 -> False (single repetition)
    """
    str_num = str(number)
    length = len(str_num)

    # Check all possible substring lengths that divide the total length
    for substring_length in range(1, length // 2 + 1):
        if length % substring_length == 0:
            substring = str_num[:substring_length]
            repetitions = length // substring_length

            # Verify the entire string is made of this substring repeated
            if substring * repetitions == str_num and repetitions >= 2:
                return True

    return False


def parse_ranges(data: str) -> list[tuple[int, int]]:
    """
    Parse input data into a list of (start, end) tuples.

    Args:
        data: Input string with ranges separated by commas (e.g., "1-10,20-30")

    Returns:
        List of (start, end) tuples

    Raises:
        ValueError: If input format is invalid
    """
    try:
        range_strings = data.strip().split(',')
        ranges = []

        for range_str in range_strings:
            start_str, end_str = range_str.strip().split('-', 1)
            start = int(start_str)
            end = int(end_str)
            ranges.append((start, end))

        return ranges
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid range format in '{data}'. Expected: 'start-end,start-end'") from e


def solve_part_1(data: str) -> int:
    """
    Find all invalid IDs that consist of exactly two repetitions of a substring.

    An ID is invalid if it follows the pattern ABCABC where:
    - A, B, C are sequences of digits
    - The two halves are identical

    Args:
        data: Input string with ranges (e.g., "1-100,200-300")

    Returns:
        Sum of all invalid IDs found

    Examples:
        "55-55" -> 55 (single invalid ID)
        "10-99" -> sum of all double-repetition numbers in range
    """
    try:
        ranges = parse_ranges(data)
    except ValueError as e:
        raise ValueError(f"Failed to parse input data: {e}") from e

    invalid_ids = []

    for start, end in ranges:
        # Validate range
        if start > end:
            raise ValueError(f"Invalid range: start ({start}) > end ({end})")

        # Find invalid IDs in this range
        for number in range(start, end + 1):
            if is_double_repetition(number):
                invalid_ids.append(number)

    return sum(invalid_ids)


def solve_part_2(data: str) -> int:
    """
    Find all invalid IDs that consist of multiple repetitions of a substring.

    An ID is invalid if it follows patterns like:
    - ABCABC (2 repetitions)
    - ABCABCABC (3 repetitions)
    - AAAAAAA (7 repetitions of single digit)

    Args:
        data: Input string with ranges (e.g., "1-100,200-300")

    Returns:
        Sum of all invalid IDs found

    Examples:
        "55-55" -> 55 (single invalid ID)
        "10-99" -> sum of all multi-repetition numbers in range
    """
    try:
        ranges = parse_ranges(data)
    except ValueError as e:
        raise ValueError(f"Failed to parse input data: {e}") from e

    invalid_ids = []

    for start, end in ranges:
        # Validate range
        if start > end:
            raise ValueError(f"Invalid range: start ({start}) > end ({end})")

        # Find invalid IDs in this range
        for number in range(start, end + 1):
            if is_multiple_repetition(number):
                invalid_ids.append(number)

    return sum(invalid_ids)


def load_input(filepath: str = "input.txt") -> str:
    """
    Load input data from file with error handling.

    Args:
        filepath: Path to the input file

    Returns:
        File contents as string

    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file can't be read
    """
    try:
        with open(filepath, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file '{filepath}' not found")
    except IOError as e:
        raise IOError(f"Error reading file '{filepath}': {e}")


if __name__ == "__main__":
    try:
        data = load_input()

        result_part_1 = solve_part_1(data)
        result_part_2 = solve_part_2(data)

        print(f"Part 1: {result_part_1}")
        print(f"Part 2: {result_part_2}")

    except (FileNotFoundError, IOError, ValueError) as error:
        print(f"Error: {error}")
        exit(1)
