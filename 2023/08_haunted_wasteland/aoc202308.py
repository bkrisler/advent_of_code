"""AoC 8, 2023: Haunted Wasteland."""

# Standard library imports
import pathlib
import re
import sys
from collections import defaultdict


def parse_data(puzzle_input):
    """Parse input."""
    nodes = {}
    for idx, row in enumerate(puzzle_input.split('\n')):
        if idx == 0:
            nodes['navigate'] = row
        elif idx == 1:
            continue
        else:
            res = re.findall(r"(\w+) = .(\w+), (\w+).", row)
            nodes[res[0][0]] = {'L': res[0][1], 'R': res[0][2]}

    return nodes


def part1(data):
    """Solve part 1."""
    print()
    nav = [*data['navigate']]
    nxt_node = 'AAA'
    sz = len(nav)
    steps = idx = 0
    while idx <= sz:
        nxt_node = data[nxt_node][nav[idx]]
        steps += 1
        idx += 1
        if nxt_node == 'ZZZ':
            break
        if idx == sz:
            idx = 0

    return steps


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
