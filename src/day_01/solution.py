#!/usr/bin/env python3
"""Day 1, 2025"""

def solve_part_1(data: str) -> int:
    lines = data.strip().split('\n')
    initial_value = 50
    count_zero = 0
    for line in lines:
        if line.startswith('L'):
            click_value = int(line[1:])
            difference = initial_value - click_value
            if difference < 0:
                initial_value = 99 + difference
            else:
                initial_value -= click_value
        elif line.startswith('R'):
            click_value = int(line[1:])
            difference = initial_value + click_value
            if difference > 99:
                initial_value = difference - 100
            else:
                initial_value += click_value
        if initial_value == 0:
            count_zero += 1

    return count_zero

def solve_part_2(data: str) -> int:
    lines = data.strip().split('\n')
    initial_value = 50
    count_zero = 0
    print(f"DEBUG: Starting with initial_value = {initial_value}")

    for line_num, line in enumerate(lines, 1):
        print(f"DEBUG: Line {line_num}: Processing '{line}'")

        if line.startswith('L'):
            click_value = int(line[1:])
            prev_value = initial_value
            print(f"DEBUG: L operation - click_value = {click_value}, current initial_value = {initial_value}")

            # Simulate step-by-step movement for left rotation
            for step in range(1, click_value + 1):
                current_pos = (prev_value - step) % 100
                print(f"DEBUG: Step {step}: {prev_value} -> {current_pos}")
                if current_pos == 0:
                    count_zero += 1
                    print(f"DEBUG: *** ZERO REACHED during rotation! count_zero is now {count_zero} ***")

            initial_value = (prev_value - click_value) % 100
            print(f"DEBUG: L final result - ({prev_value} - {click_value}) % 100 = {initial_value}")

        elif line.startswith('R'):
            click_value = int(line[1:])
            prev_value = initial_value
            print(f"DEBUG: R operation - click_value = {click_value}, current initial_value = {initial_value}")

            # Simulate step-by-step movement for right rotation
            for step in range(1, click_value + 1):
                current_pos = (prev_value + step) % 100
                print(f"DEBUG: Step {step}: {prev_value} -> {current_pos}")
                if current_pos == 0:
                    count_zero += 1
                    print(f"DEBUG: *** ZERO REACHED during rotation! count_zero is now {count_zero} ***")

            initial_value = (prev_value + click_value) % 100
            print(f"DEBUG: R final result - ({prev_value} + {click_value}) % 100 = {initial_value}")

        print(f"DEBUG: After operation, initial_value = {initial_value}")
        print("---")

    print(f"DEBUG: Final result - count_zero = {count_zero}")
    return count_zero

if __name__ == "__main__":
    with open("input.txt") as f:
        data = f.read()

    print("=== SOLUTION COMPARISON ===")
    print(f"Part 1 (final position only): {solve_part_1(data)}")
    print(f"Part 2 (step-by-step counting): {solve_part_2(data)}")
