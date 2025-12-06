#!/usr/bin/env python3
"""Day 5, 2025"""

def solve_part_1(data: str) -> int:
    lines = data.strip().split("\n")
    blank_line_index = lines.index("")
    ids = lines[blank_line_index+1:]
    ranges = lines[:blank_line_index]
    fresh_count = 0
    range_map = {}
    for r in ranges:
        [low, high] = r.split("-")
        range_map[r] = [int(low), int(high)]
    for id in ids:
        fresh = False
        for r in range_map:
            [low, high] = range_map[r]
            if low <= int(id) <= high:
                fresh= True
                break
        if fresh:
            fresh_count += 1
    return fresh_count

def solve_part_2(data: str) -> int:
  # Initialize variables:
  # - fresh_ranges: stores parsed number ranges as [start, end] pairs
  # - highest: tracks the highest number processed so far (to avoid double-counting)
  # - a: accumulator for total count of numbers covered by ranges
  fresh_ranges, highest, a = [], 0, 0

  # Parse input lines to extract ranges
  for line in data.strip().split("\n"):
    if "-" in line:
      # Split hyphen-separated ranges and convert to integers
      fresh_ranges.append(list(map(int, line.split("-"))))

  # Process ranges in sorted order to efficiently calculate coverage
  for start, end in sorted(fresh_ranges):
    if start > highest:
      # Non-overlapping range: add full range length
      a += end - start + 1
    elif end > highest:
      # Overlapping range: add only the new portion beyond current highest
      a += end - highest
    # Update highest to the furthest point covered so far
    highest = max(highest, end)

  return a



if __name__ == "__main__":
    with open("input.txt") as f:
        data = f.read()

    print(f"Part 1: {solve_part_1(data)}")
    print(f"Part 2: {solve_part_2(data)}")
