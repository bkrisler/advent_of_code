"""AoC 7, 2024: bridge_repair."""
import itertools
# Standard library imports
import pathlib
import sys


def parse_data(puzzle_input):
    """Parse input."""
    results = []
    for line in puzzle_input.split('\n'):
        parts = line.split(':')
        goal = int(parts[0])
        operators = [int(x) for x in parts[1].split()]
        results.append([goal, operators])

    return results

def act(op, a, b):
    if op == '*':
        return a * b
    elif op == '+':
        return a + b

    return 0



def part1(data):
    """Solve part 1."""
    print()
    result = 0
    for row in data:
        result += process_entry(result, row)

    return result


def process_entry(result, row):
    goal = row[0]
    values = row[1]
    operators = list(itertools.product('*+', repeat=len(values) - 1))
    for ooo in operators:
        result = compute(ooo, values)
        if result == goal:
            return result

    return 0


def compute(ooo, values):
    result = values[0]
    for idx, v in enumerate(values[1:]):
        result = eval(f'{result} {ooo[idx]} {v}')

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
