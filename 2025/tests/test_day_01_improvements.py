#!/usr/bin/env python3
"""Test script to verify that the improved solution produces correct results."""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from solution import solve_part_1 as original_part1, solve_part_2 as original_part2
from solution_improved import (
    solve_part_1_optimized as improved_part1,
    solve_part_2_optimized as improved_part2_sim,
    solve_part_2_mathematical as improved_part2_math
)


def test_solutions():
    """Test that all solutions produce consistent results."""

    # Test with the provided test input
    test_file = "test-input.txt"

    if not os.path.exists(test_file):
        print("Test input file not found, using sample data")
        sample_data = "R5\nL3\nR2\nL1\n"
    else:
        with open(test_file) as f:
            sample_data = f.read()

    print("=== TESTING SOLUTION CONSISTENCY ===")
    print(f"Input data:\n{sample_data}")
    print("-" * 40)

    # Test Part 1
    print("\nPart 1 Testing:")
    try:
        original_result1 = original_part1(sample_data)
        improved_result1 = improved_part1(sample_data)

        print(f"Original solution:     {original_result1}")
        print(f"Improved solution:     {improved_result1}")
        print(f"Results match:         {'✓' if original_result1 == improved_result1 else '✗'}")

        if original_result1 != improved_result1:
            print("ERROR: Part 1 results don't match!")
            return False
    except Exception as e:
        print(f"Part 1 error: {e}")
        return False

    # Test Part 2
    print("\nPart 2 Testing:")
    try:
        original_result2 = original_part2(sample_data)
        improved_result2_sim = improved_part2_sim(sample_data)
        improved_result2_math = improved_part2_math(sample_data)

        print(f"Original solution:           {original_result2}")
        print(f"Improved simulation:         {improved_result2_sim}")
        print(f"Improved mathematical:       {improved_result2_math}")
        print(f"Original vs Simulation:      {'✓' if original_result2 == improved_result2_sim else '✗'}")
        print(f"Simulation vs Mathematical:  {'✓' if improved_result2_sim == improved_result2_math else '✗'}")

        if original_result2 != improved_result2_sim:
            print("ERROR: Part 2 results don't match!")
            return False
        if improved_result2_sim != improved_result2_math:
            print("ERROR: Part 2 internal consistency check failed!")
            return False

    except Exception as e:
        print(f"Part 2 error: {e}")
        return False

    print("\n✓ All tests passed! Solutions are consistent.")
    return True


def test_error_handling():
    """Test that error handling works correctly."""

    print("\n=== TESTING ERROR HANDLING ===")

    # Test invalid input
    invalid_inputs = [
        "X5",      # Invalid operation
        "Labc",    # Invalid number
        "L-5",     # Negative number
        "",        # Empty input
        "L\nR\n",  # Empty lines
    ]

    for i, invalid_input in enumerate(invalid_inputs):
        try:
            improved_part1(invalid_input)
            print(f"Test {i+1}: ERROR - Should have failed for: {repr(invalid_input)}")
            return False
        except Exception as e:
            print(f"Test {i+1}: ✓ Correctly rejected {repr(invalid_input)} - {e}")

    print("✓ Error handling tests passed!")
    return True


def test_edge_cases():
    """Test edge cases and boundary conditions."""

    print("\n=== TESTING EDGE CASES ===")

    edge_cases = [
        ("L0", "Zero steps"),
        ("R0", "Zero steps"),
        ("L100", "Full rotation"),
        ("R100", "Full rotation"),
        ("L99", "Near full rotation"),
        ("R99", "Near full rotation"),
    ]

    for input_data, description in edge_cases:
        try:
            result1 = improved_part1(input_data)
            result2_sim = improved_part2_sim(input_data)
            result2_math = improved_part2_math(input_data)

            print(f"{description:25} - P1: {result1}, P2-Sim: {result2_sim}, P2-Math: {result2_math}")

            # Verify consistency
            if result2_sim != result2_math:
                print(f"  ERROR: Inconsistent results for {description}")
                return False

        except Exception as e:
            print(f"{description:25} - Error: {e}")
            return False

    print("✓ Edge case tests passed!")
    return True


def performance_test():
    """Simple performance comparison."""

    print("\n=== PERFORMANCE COMPARISON ===")

    # Create a large test case
    large_test = "\n".join([f"L{i%50+1}" for i in range(1000)]) + "\n" + \
                 "\n".join([f"R{i%50+1}" for i in range(1000)])

    import time

    # Time original solutions
    start_time = time.time()
    orig_result1 = original_part1(large_test)
    orig_time1 = time.time() - start_time

    start_time = time.time()
    orig_result2 = original_part2(large_test)
    orig_time2 = time.time() - start_time

    # Time improved solutions
    start_time = time.time()
    imp_result1 = improved_part1(large_test)
    imp_time1 = time.time() - start_time

    start_time = time.time()
    imp_result2_sim = improved_part2_sim(large_test)
    imp_time2_sim = time.time() - start_time

    start_time = time.time()
    imp_result2_math = improved_part2_math(large_test)
    imp_time2_math = time.time() - start_time

    print(f"Large test case (2000 operations):")
    print(f"Original Part 1:     {orig_time1:.4f}s -> {orig_result1}")
    print(f"Improved Part 1:     {imp_time1:.4f}s -> {imp_result1}")
    print(f"Original Part 2:     {orig_time2:.4f}s -> {orig_result2}")
    print(f"Improved Part 2 Sim: {imp_time2_sim:.4f}s -> {imp_result2_sim}")
    print(f"Improved Part 2 Math:{imp_time2_math:.4f}s -> {imp_result2_math}")

    # Verify results match
    if orig_result1 != imp_result1 or orig_result2 != imp_result2_sim:
        print("ERROR: Results don't match!")
        return False

    print("✓ Performance test completed!")
    return True


def main():
    """Run all tests."""

    print("Running comprehensive tests for improved solution...\n")

    tests = [
        test_solutions,
        test_error_handling,
        test_edge_cases,
        performance_test,
    ]

    for test in tests:
        if not test():
            print(f"\n❌ Test failed: {test.__name__}")
            return 1

    print("\n🎉 All tests passed! The improved solution is working correctly.")
    return 0


if __name__ == "__main__":
    exit(main())
