#!/usr/bin/env python3
"""Day 4, 2025"""

def solve_part_1(data: str) -> str:
    # Parse input into a 2D grid
    lines = data.strip().split('\n')
    grid = [list(line) for line in lines]

    # Define all 8 possible neighbors (including diagonals)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    # Function to count adjacent '@' symbols
    def count_adjacent_rolls(x, y):
        count = 0
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Check if neighbor is within grid bounds and is a roll
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == '@':
                count += 1
        return count

    # Create new grid for output, initially same as input
    result_grid = [row.copy() for row in grid]

    # Count of accessible rolls
    accessible_count = 0

    # Check each cell in the grid
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '@':
                # Count adjacent rolls
                adjacent_count = count_adjacent_rolls(i, j)
                # If fewer than 4 adjacent rolls, mark as accessible
                if adjacent_count < 4:
                    result_grid[i][j] = 'x'
                    accessible_count += 1

    # Convert result grid to string
    result = '\n'.join([''.join(row) for row in result_grid])

    # Add a note about the count of accessible rolls
    result += f"\n\nThere are {accessible_count} rolls of paper that can be accessed by a forklift."

    return result

def solve_part_2(data: str) -> int:
    # Parse input into a 2D grid
    lines = data.strip().split('\n')
    grid = [list(line) for line in lines]

    # Define all 8 possible neighbors (including diagonals)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    # Function to count adjacent '@' symbols
    def count_adjacent_rolls(x, y):
        count = 0
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Check if neighbor is within grid bounds and is a roll
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == '@':
                count += 1
        return count

    # Total count of removed rolls
    total_removed = 0

    # Continue until no more rolls can be removed
    while True:
        # Find all accessible rolls in the current grid
        accessible_rolls = []

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == '@':
                    # Count adjacent rolls
                    adjacent_count = count_adjacent_rolls(i, j)
                    # If fewer than 4 adjacent rolls, it's accessible
                    if adjacent_count < 4:
                        accessible_rolls.append((i, j))

        # If no accessible rolls, we're done
        if not accessible_rolls:
            break

        # Remove all accessible rolls
        for i, j in accessible_rolls:
            grid[i][j] = '.'  # Mark as empty

        total_removed += len(accessible_rolls)

    return total_removed

if __name__ == "__main__":
    with open("input.txt") as f:
        data = f.read()

    print(f"Part 1:\n{solve_part_1(data)}")
    print(f"Part 2: {solve_part_2(data)}")
