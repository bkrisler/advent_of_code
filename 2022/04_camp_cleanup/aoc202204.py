"""AoC 4, 2022: camp_cleanup."""

# Standard library imports
import pathlib
import sys
import re
import numpy as np


def parse_data(puzzle_input):
    """Parse input."""
    pattern = re.compile('(\d*)-(\d*),(\d*)-(\d*)')
    return [(np.arange(int(s[0]), int(s[1])+1), np.arange(int(s[2]), int(s[3])+1)) for s in re.findall(pattern, puzzle_input)]


def part1(data):
    """Solve part 1."""
    counter = 0
    for d in data:
        counter += 1 if np.all(np.isin(d[0], d[1]) == True) or np.all(np.isin(d[1], d[0]) == True) else 0

    return counter


def part2(data):
    """Solve part 2."""
    counter = 0
    for d in data:
        counter += 1 if np.any(np.isin(d[0], d[1]) == True) or np.any(np.isin(d[1], d[0]) == True) else 0

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
