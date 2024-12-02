"""AoC 2, 2024: red_nosed_reports."""

# Standard library imports
import pathlib
import sys


def parse_data(puzzle_input):
    """Parse input."""
    reports = []
    for row in puzzle_input.split('\n'):
        level = [int(x) for x in row.split(' ')]
        reports.append(level)
    return reports

def part1(data):
    """Solve part 1."""
    counts = 0
    for report in data:
        diff_list = []
        sign = []
        for idx in range(1, len(report)):
            if report[idx-1] > report[idx]:
                sign.append(-1)
            else:
                sign.append(1)
            diff_list.append(abs(report[idx-1] - report[idx]))
        if (all(x > 0 for x in diff_list) and
            all(x < 4 for x in diff_list)) and all(x == sign[0] for x in sign):
                counts += 1
    return counts

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
