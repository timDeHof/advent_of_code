#!/usr/bin/env python3
"""Day 7, 2025"""
from typing import Set, Tuple

def solve_part_1(data: str) -> int:
    """Count how many times beams are split by splitters (^).
    
    Beams move downward. When a beam hits a splitter, it stops and creates
    two new beams moving downward from left and right of the splitter.
    Multiple beams can hit the same splitter, but we only count it once.
    """
    manifold = data.strip().split('\n')
    H = len(manifold)
    W = len(manifold[0])

    # Find starting position S
    sx = sy = None
    for y, row in enumerate(manifold):
        if 'S' in row:
            sx = row.index('S')
            sy = y
            break
    if sx is None or sy is None:
        raise ValueError("No starting point found")

    # Track active beam positions
    active: Set[Tuple[int, int]] = set()
    if sy + 1 < H:
        active.add((sx, sy + 1))

    splits = 0

    # Simulate beams moving downward
    while active:
        next_active: Set[Tuple[int, int]] = set()
        split_events: Set[Tuple[int, int]] = set()

        for x, y in active:
            if not (0 <= x < W and 0 <= y < H):
                continue

            cell = manifold[y][x]
            if cell == '^':
                # Beam hits a splitter
                split_events.add((x, y))
            else:
                # Beam continues downward through empty space
                ny = y + 1
                if ny < H:
                    next_active.add((x, ny))

        # Count each unique splitter hit this step
        splits += len(split_events)

        # Create new beams from splitters (left and right, one row down)
        for x, y in split_events:
            ny = y + 1
            if ny < H:
                if x - 1 >= 0:
                    next_active.add((x - 1, ny))
                if x + 1 < W:
                    next_active.add((x + 1, ny))

        active = next_active

    return splits


def solve_part_2(data: str) -> int:
    """Count total timelines in quantum tachyon splitting.
    
    A single particle takes both paths at each splitter, creating parallel timelines.
    Key insight: track how many timelines are at each position. When N timelines
    hit a splitter, it creates N additional timelines (one per original timeline).
    Start with 1 timeline and add the count each time timelines hit a splitter.
    """
    manifold = data.strip().split('\n')
    H = len(manifold)
    W = len(manifold[0])

    # Find starting position S
    sx = sy = None
    for y, row in enumerate(manifold):
        if 'S' in row:
            sx = row.index('S')
            sy = y
            break

    # Track position -> number of timelines at that position
    active = {(sx, sy + 1): 1} if sy + 1 < H else {}
    timelines = 1  # Start with 1 timeline from S

    while active:
        next_active = {}

        for (x, y), count in active.items():
            if not (0 <= x < W and 0 <= y < H):
                continue

            cell = manifold[y][x]
            if cell == '^':
                # Each timeline hitting this splitter creates an additional timeline
                timelines += count
                ny = y + 1
                if ny < H:
                    # Split: each timeline goes both left and right
                    if x - 1 >= 0:
                        next_active[(x - 1, ny)] = next_active.get((x - 1, ny), 0) + count
                    if x + 1 < W:
                        next_active[(x + 1, ny)] = next_active.get((x + 1, ny), 0) + count
            else:
                # Continue downward through empty space
                ny = y + 1
                if ny < H:
                    next_active[(x, ny)] = next_active.get((x, ny), 0) + count

        active = next_active

    return timelines

if __name__ == "__main__":
    with open("input.txt") as f:
        data = f.read()

    print(f"Part 1: {solve_part_1(data)}")
    print(f"Part 2: {solve_part_2(data)}")

