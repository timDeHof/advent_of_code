#!/usr/bin/env python3
"""Debug test for the step-by-step counting logic"""

def test_step_by_step_counting():
    # Test data from the example
    test_data = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

    lines = test_data.strip().split('\n')
    initial_value = 50
    count_zero = 0

    print(f"Starting at position: {initial_value}")
    print("=" * 50)

    for line_num, line in enumerate(lines, 1):
        print(f"\nStep {line_num}: {line}")
        print(f"Starting position: {initial_value}")

        if line.startswith('L'):
            click_value = int(line[1:])
            zeros_in_this_rotation = 0

            # Simulate step-by-step movement for left rotation
            for step in range(1, click_value + 1):
                current_pos = (initial_value - step) % 100
                print(f"  Step {step}: {initial_value} -> {current_pos}")
                if current_pos == 0:
                    count_zero += 1
                    zeros_in_this_rotation += 1
                    print(f"    *** ZERO REACHED! Total count: {count_zero} ***")

            initial_value = (initial_value - click_value) % 100
            print(f"Final position after L{click_value}: {initial_value}")
            print(f"Zeros found in this rotation: {zeros_in_this_rotation}")

        elif line.startswith('R'):
            click_value = int(line[1:])
            zeros_in_this_rotation = 0

            # Simulate step-by-step movement for right rotation
            for step in range(1, click_value + 1):
                current_pos = (initial_value + step) % 100
                print(f"  Step {step}: {initial_value} -> {current_pos}")
                if current_pos == 0:
                    count_zero += 1
                    zeros_in_this_rotation += 1
                    print(f"    *** ZERO REACHED! Total count: {count_zero} ***")

            initial_value = (initial_value + click_value) % 100
            print(f"Final position after R{click_value}: {initial_value}")
            print(f"Zeros found in this rotation: {zeros_in_this_rotation}")

    print("\n" + "=" * 50)
    print(f"FINAL RESULT: {count_zero}")
    print(f"Expected: 3")
    print(f"Match: {count_zero == 3}")

if __name__ == "__main__":
    test_step_by_step_counting()
