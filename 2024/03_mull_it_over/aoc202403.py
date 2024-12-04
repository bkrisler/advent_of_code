"""AoC 3, 2024: mull_it_over."""

# Standard library imports
import pathlib
import re
import sys


def parse_data(puzzle_input):
    """Parse input."""
    p = re.compile("mul\(\d{1,3},\d{1,3}\)")
    result = p.findall(puzzle_input)
    return result


def part1(data):
    """Solve part 1."""
    p = re.compile("mul\((\d{1,3}),(\d{1,3})\)")
    result = 0
    for r in data:
        m = p.match(r)
        result += int(m.group(1)) * int(m.group(2))
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
