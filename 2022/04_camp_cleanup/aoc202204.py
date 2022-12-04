"""AoC 4, 2022: camp_cleanup."""

# Standard library imports
import pathlib
import sys
import re
import numpy as np


def parse_data(puzzle_input):
    """Parse input."""
    pattern = re.compile('(\d*)-(\d*),(\d*)-(\d*)')
    sections = re.findall(pattern, puzzle_input)
    groups = []
    for section in sections:
        group1 = list(range(int(section[0]), int(section[1])+1))
        group2 = list(range(int(section[2]), int(section[3])+1))
        groups.append((group1, group2))
    return groups


def part1(data):
    """Solve part 1."""
    counter = 0
    for group in data:
        a = np.array(group[0])
        b = np.array(group[1])
        if np.all(np.isin(a, b) == True) or np.all(np.isin(b, a) == True):
            counter += 1

    return counter


def part2(data):
    """Solve part 2."""
    counter = 0
    for group in data:
        a = np.array(group[0])
        b = np.array(group[1])
        if np.any(np.isin(a, b) == True) or np.any(np.isin(b, a) == True):
            counter += 1

    return counter


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse_data(puzzle_input)
    yield part1(data)
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().strip())
        print("\n".join(str(solution) for solution in solutions))
