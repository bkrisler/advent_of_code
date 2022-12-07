"""AoC 6, 2022: tuning_trouble."""

# Standard library imports
import pathlib
import sys


def add(x, item, size=4):
    if len(x) >= size:
        x = x[1:]
    x.append(item)

    return x


def parse_data(puzzle_input):
    """Parse input."""
    return puzzle_input


def part1(data):
    """Solve part 1."""
    buffer = []
    for cnt, val in enumerate(data):
        buffer = add(buffer, val)
        if len(buffer) == 4 and len(set(buffer)) == 4:
            return cnt + 1
    return None


def part2(data):
    """Solve part 2."""
    buffer = []
    for cnt, val in enumerate(data):
        buffer = add(buffer, val, 14)
        if len(buffer) == 14 and len(set(buffer)) == 14:
            return cnt + 1
    return None


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
