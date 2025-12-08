#!/usr/bin/env python3
"""Day 8, 2025"""
import collections
import functools
import itertools

Pos = tuple[int, int, int]

def parse_input(data: str) -> list[Pos]:
    """Parse input into list of 3D positions."""
    return [parse_line(line) for line in data.strip().split('\n')]

def parse_line(line: str) -> Pos:
    """Parse a single line 'x,y,z' into a 3D position tuple."""
    res = tuple(int(_) for _ in line.split(','))
    assert len(res) == 3
    return res

def get_distance(a: Pos, b: Pos) -> int:
    """Calculate squared Euclidean distance between two 3D positions."""
    return sum((_a - _b) ** 2 for _a, _b in zip(a, b, strict=True))

def sort_by_distance(positions: list[Pos]) -> list[tuples[Pos,Pos]]:
    """Generate all position pairs sorted by distance (closest first)."""
    return sorted(itertools.combinations(positions, 2), key=lambda x: get_distance(*x))

def _limit(positions: list[Pos]) -> int:
  """Determine connection limit based on input size (test vs real input)."""
  if len(positions) == 20:
    return 10
  return 1000

def _connect(circuits: dict[Pos, int], pos_a: Pos, pos_b: Pos) -> None:
    """Merge two circuit groups using union-find algorithm."""
    if circuits[pos_a] != circuits[pos_b]:
        circuit_b = circuits[pos_b]
        for pos in circuits:
            if circuits[pos] == circuit_b:
                circuits[pos] = circuits[pos_a]

def _top_3(circuits: dict[Pos, int]) -> list[int]:
  """Get sizes of the three largest circuit groups."""
  counter = collections.Counter(circuits.values())
  x = sorted(counter.values(), reverse=True)

  return x[:3]

def _score(circuits: dict[Pos,int]) -> int:
    """Calculate score by multiplying sizes of top 3 circuit groups."""
    return functools.reduce(lambda a, b: a * b, _top_3(circuits))

def solve_part_1(data: str) -> int:
    """Connect closest position pairs up to limit, return product of top 3 group sizes."""
    positions = parse_input(data)
    circuits = {_p: _n for _n, _p in enumerate(positions)}
    connections = sort_by_distance(positions)[: _limit(positions)]
    for c in connections:
        _connect(circuits, *c)
    return _score(circuits)

def _are_connected(circuits: dict[Pos, int]) -> bool:
    """Check if all positions are in a single connected circuit."""
    return len(set(circuits.values())) == 1

def solve_part_2(data: str) -> int:
    """Find the connection that unifies all positions, return product of first coordinates."""
    positions = parse_input(data)
    circuits = {_p: _n for _n, _p in enumerate(positions)}
    connections = sort_by_distance(positions)
    connecting = None
    for c in connections:
        _connect(circuits, *c)
        if _are_connected(circuits):
            connecting = c
            break
    assert connecting is not None
    return connecting[0][0] * connecting[1][0]

if __name__ == "__main__":
    with open("input.txt") as f:
        data = f.read()

    print(f"Part 1: {solve_part_1(data)}")
    print(f"Part 2: {solve_part_2(data)}")
