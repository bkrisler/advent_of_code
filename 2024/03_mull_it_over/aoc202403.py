"""AoC 3, 2024: mull_it_over."""

# Standard library imports
import pathlib
import re
import sys


def parse_data(puzzle_input):
    """Parse input."""
    return puzzle_input


def part1(data):
    """Solve part 1."""
    p = re.compile("mul\((\d{1,3}),(\d{1,3})\)")
    return sum([int(r[0]) * int(r[1]) for r in p.findall(data)])

def sum_multipliers(line):
    p = re.compile("mul\((\d{1,3}),(\d{1,3})\)")
    return sum([int(r[0]) * int(r[1]) for r in p.findall(line)])

def part2(data):
    """Solve part 2."""
    parts = data.split("don't")
    if len(parts) == 0:
        return 0

    total = sum_multipliers(parts[0])
    for part in parts[1:]:
        sub_parts = part.split('do()')
        if len(sub_parts) == 1:
            continue
        else:
            for sp in sub_parts[1:]:
                total += sum_multipliers(sp)

    return total

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
