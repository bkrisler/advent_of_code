"""AoC 5, 2024: print_queue."""
import functools
import math
# Standard library imports
import pathlib
import sys


def parse_data(puzzle_input):
    """Parse input."""
    stage_one = [x for x in puzzle_input.split('\n\n')]
    stage_two = [x for x in stage_one[0].split('\n')]
    global order_rules
    order_rules = {}
    for x in stage_two:
        parts = x.split('|')
        if parts[0] in order_rules:
            order_rules[parts[0]].append(parts[1])
        else:
            order_rules[parts[0]] = [parts[1]]
    data = []
    for row in stage_one[1].split('\n'):
        data.append([x for x in row.split(',')])
    return data

def compare(x, y):
    if x in order_rules:
        lookup_x = order_rules[x]
        if y in lookup_x:
            return -1

    if y in order_rules:
        lookup_y = order_rules[y]
        if x in lookup_y:
            return 1

    return 0

def part1(data):
    """Solve part 1."""
    print()
    total = 0
    for row in data:
        sorted_pages = sorted(row, key=functools.cmp_to_key(compare))
        if row == sorted_pages:
            middle = math.ceil(len(row)/2) - 1
            total += int(row[middle])

    return total

def part2(data):
    """Solve part 2."""
    print()
    total = 0
    for row in data:
        sorted_pages = sorted(row, key=functools.cmp_to_key(compare))
        if row != sorted_pages:
            middle = math.ceil(len(sorted_pages)/2) - 1
            total += int(sorted_pages[middle])

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
