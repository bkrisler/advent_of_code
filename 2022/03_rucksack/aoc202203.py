"""AoC 3, 2022: rucksack."""

# Standard library imports
import pathlib
import sys
import numpy as np
import string
from functools import reduce


def parse_data(puzzle_input):
    """Parse input."""
    return [list(x) for x in puzzle_input.splitlines()]


def find_duplicates(a_list):
    u, c = np.unique(a_list, return_counts=True)
    return u[c > 1].tolist()


def get_priority(item):
    priority = string.ascii_lowercase.index(str(item[0]).lower()) + 1
    priority += 26 if str(item[0]).isupper() else 0
    return priority


def part1(data):
    """Solve part 1."""
    priorities = []
    for sack in data:
        sides = np.split(np.asarray(sack), 2)
        priorities.append(get_priority(np.intersect1d(sides[0], sides[1])))

    return sum(priorities)


def part2(data):
    """Solve part 2."""
    groups = [data[i:i + 3] for i in range(0, len(data), 3)]
    priorities = []
    for group in groups:
        x = reduce(np.intersect1d, (group[0], group[1], group[2]))
        priorities.append(get_priority(str(x[0])))

    return sum(priorities)


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
