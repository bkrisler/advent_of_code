"""AoC 1, 2018: frequency"""

# Standard library imports
import pathlib
import sys
from itertools import cycle


def parse_data(puzzle_input):
    """Parse input."""
    return list(map(int, puzzle_input.split()))


def part1(data):
    """Solve part 1."""
    return sum(data)


def part2(data):
    """Solve part 2."""
    observed = set([0])
    crnt = 0
    for freq in cycle(data):
        try:
            crnt += freq
            if crnt in observed:
                return crnt
            else:
                observed.add(crnt)
        except IndexError:
            observed.add(freq)


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
