#!/usr/bin/env python3
"""Day 3, 2025"""

def solve_part_1(data: str) -> int:
    """
    Find the maximum voltage that can be produced from battery combinations.

    For each line, find the maximum sum of any two battery ratings (digits 1-9).
    Return the sum of these maximum values across all lines.
    """
    lines = data.strip().split('\n')
    total_max_voltage = 0

    for line in lines:
        # Convert line to list of integers (battery ratings)
        batteries = list(map(str, line.strip()))
        # Find maximum sum of any two batteries
        max_voltage = 0
        for i in range(len(batteries)):
            for j in range(i + 1, len(batteries)):
                voltage = batteries[i] + batteries[j]
                max_voltage = max(max_voltage, int(voltage))

        total_max_voltage += max_voltage

    return total_max_voltage

def solve_part_2(data: str) -> int:
    """
    Find the maximum voltage that can be produced from battery combinations.

    For each line, select exactly 12 batteries in order to form the largest
    possible 12-digit number. Return the sum of these maximum values across all lines.
    """
    lines = data.strip().split('\n')
    total_output_voltage = 0

    for line in lines:
        batteries = list(map(int, line.strip()))
        n = len(batteries)

        # Find the largest 12-digit number by selecting exactly 12 batteries in order
        if n <= 12:
            voltage_str = "".join(map(str, batteries))
        else:
            # Use a greedy approach: at each step, choose the largest possible digit
            # that allows us to still select enough digits for the remaining positions
            result = []
            start_idx = 0
            remaining_positions = 12

            for pos in range(12):
                # We need to leave enough digits for the remaining positions
                end_idx = n - remaining_positions + 1

                # Find the maximum digit in the valid range
                max_digit = max(batteries[start_idx:end_idx])
                max_idx = batteries[start_idx:end_idx].index(max_digit) + start_idx

                result.append(str(max_digit))
                start_idx = max_idx + 1
                remaining_positions -= 1

                if start_idx >= n:
                    break

            voltage_str = "".join(result)

        voltage_int = int(voltage_str)
        total_output_voltage += voltage_int

    return total_output_voltage

if __name__ == "__main__":
    with open("input.txt") as f:
        data = f.read()

    print(f"Part 1: {solve_part_1(data)}")
    print(f"Part 2: {solve_part_2(data)}")
