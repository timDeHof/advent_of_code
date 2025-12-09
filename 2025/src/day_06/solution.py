#!/usr/bin/env python3
"""Day 6, 2025"""
import numpy as np
import operator
print(np.__version__)
def solve_part_1(data: str) -> int:
    lines = data.strip().split('\n')
    parsed_lines = [line.split() for line in lines]

    numbers = np.array([[int(x) for x in row] for row in parsed_lines[:-1]])
    operations = parsed_lines[-1]

    results = []
    for i, op in enumerate(operations):
        nums = numbers[:, i]
        result = nums[0]
        for num in nums[1:]:
            result = result + num if op == '+' else result * num
        results.append(result)

    return sum(results)

def solve_part_2(data: str) -> int:
    """
    Solves part 2 of the problem by processing a grid of numbers with operations.

    The input data is organized as a grid where:
    - Upper rows contain numbers (possibly split across multiple rows)
    - Bottom row contains operation symbols (+ or *)
    - Each column represents a separate calculation

    Returns the grand total of all column calculations.
    """
    # Split input data into individual lines
    problems = data.splitlines()

    # Index of the operations row (last row)
    ops_row_idx = len(problems) - 1

    # Initialize grand total accumulator
    grand_total = 0

    # Operation mapping: symbol -> (function, initial_value)
    ops = {
    "*": (operator.mul, 1),  # Multiplication with identity 1
    "+": (operator.add, 0)   # Addition with identity 0
    }

    # Process each column in the grid
    for col in range(len(problems[0])):
        # Check if current column has an operation symbol
        if problems[ops_row_idx][col] != " ":
            # Get the operation function and initial result value
            op, result = ops[problems[ops_row_idx][col]]

        # Build number string by concatenating characters from each row in this column
        number_str = ""
        for row in range(ops_row_idx):
            number_str += problems[row][col]

        # If we have a valid number, apply the operation
        if number_str.strip().isdigit():
            result = op(result, int(number_str))
        else:
            # If not a valid number, add current result to grand total
            grand_total += result

    # Add the final result from the last column
    grand_total += result

    return grand_total


if __name__ == "__main__":
    with open("input.txt") as f:
        data = f.read()

    print(f"Part 1: {solve_part_1(data)}")
    print(f"Part 2: {solve_part_2(data)}")
