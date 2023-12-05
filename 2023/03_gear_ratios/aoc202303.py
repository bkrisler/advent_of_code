"""AoC 3, 2023: Gear Ratios."""

# Standard library imports
import pathlib
import sys
import re
from collections import defaultdict
from io import StringIO

import numpy as np


def parse_data_np(puzzle_input):
    """Parse input."""
    matrix = np.genfromtxt(StringIO(puzzle_input), dtype='str', delimiter=1, deletechars=None, comments=None)
    return matrix


def parse_symbol_list(puzzle_input):
    symbols = []
    for c in puzzle_input:
        if c != '.' and c != '\n' and not c.isdigit() and c not in symbols:
            symbols.append(c)
    return symbols


def parse_data(puzzle_input):
    pattern = r'(\d+)'
    result = defaultdict(list)
    for idx, row in enumerate(puzzle_input.split('\n')):
        matches = re.finditer(pattern, row)
        for match in matches:
            #print("{}: [{}, ({}, {})]".format(match.group(), idx, match.start(), match.end()))
            key = (idx, match.start())
            result[key].append(int(match.group()))
            result[key].append(match.end()-match.start())

    symbols = parse_symbol_list(puzzle_input)

    return result, symbols, parse_data_np(puzzle_input)


def has_adjacent(matrix, symbols, x_coord, y_coord):

    adjacency = [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if not (i == j == 0)]
    for dx, dy in adjacency:
        if 0 <= (x_coord + dx) < np.shape(matrix)[1] and 0 <= y_coord + dy < np.shape(matrix)[1]:
            cv = matrix[x_coord + dx, y_coord + dy]
            #print("Check: {} and {}, {}".format(cv, x_coord + dx, y_coord + dy))
            if cv in symbols:
                return True

    return False


def part1(data, symbols, matrix):
    """Solve part 1."""
    print(data)
    matches = []
    for pos, part in data.items():
        has_match = False
        for x in range(pos[1], pos[1]+part[1]):
            #print("{} at {}, {}".format(part[0], pos[0], x))
            if has_adjacent(matrix, symbols, pos[0], x):
                print("Match: {}".format(part[0]))
                has_match = True
        if has_match:
            matches.append(part[0])

    print('--- Part 1 ----')
    print(sum(matches))
    print('---')



def part2(data):
    """Solve part 2."""


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data, symbols, matrix = parse_data(puzzle_input)
    yield part1(data, symbols, matrix)
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
        print("\n".join(str(solution) for solution in solutions))
