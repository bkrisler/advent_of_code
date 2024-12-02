"""AoC 1, 2024: historian_hysteria."""
# Standard library imports
import pathlib
import sys

def parse_data(puzzle_input):
    """Parse input."""
    col1 = []
    col2 = []
    for row in puzzle_input.split('\n'):
        col1.append(int(row.split()[0]))
        col2.append(int(row.split()[1]))
    return (col1, col2)

def part1(data):
    """Solve part 1."""
    col1 = sorted(data[0])
    col2 = sorted(data[1])
    result = []
    for idx, c in enumerate(col1):
        result.append(abs(c - col2[idx]))
    return sum(result)

def part2(data):
    """Solve part 2."""
    col1 = sorted(data[0])
    col2 = sorted(data[1])
    result = []
    for idx, c in enumerate(col1):
        x = col2.count(c)
        result.append(c*x)
    return sum(result)

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
