"""AoC 9, 2023: Mirage Maintenance."""

# Standard library imports
import pathlib
import sys
import numpy as np


def parse_data(puzzle_input):
    """Parse input."""
    result = []
    for row in puzzle_input.split('\n'):
        result.append([int(x) for x in row.split(' ')])
    return result


def step_difference(row):
    history = [row]
    while(np.sum(history[-1])) != 0:
        history.append(np.diff(history[-1]))

    for x in reversed(range(len(history))):
        if x == len(history)-1:
            history[x] = np.concatenate((history[x], [0]))
        else:
            history[x] = np.concatenate((history[x], [history[x+1][-1]+history[x][-1]]))

    return history[0][-1]


def part1(data):
    """Solve part 1."""
    print()
    result = 0
    for row in data:
        result += step_difference(row)

    return result


def part2(data):
    """Solve part 2."""


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse_data(puzzle_input)
    yield part1(data)
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
        print("\n".join(str(solution) for solution in solutions))
