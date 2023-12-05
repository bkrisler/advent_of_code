"""AoC 3, 2023: Gear Ratios."""

# Standard library imports
import pathlib
import sys
import re
from collections import defaultdict
from io import StringIO

import numpy as np


def find_adj(matrix, x, y, d=1):
    # Create the nearest neighbors
    x_idx, y_idx = np.mgrid[-d:d + 1, -d:d + 1]

    # Remove the center (0,0) index
    center = (x_idx == 0) & (y_idx == 0)
    x_idx = x_idx[~center]
    y_idx = y_idx[~center]
    #print("fa: {}, {}".format(x_idx+x, y_idx+y))
    res = matrix[x_idx+x, y_idx+y]

    #print("Pos: {} has adjacent: {}".format(matrix[x, y], res))

    return res


def parse_data_np(puzzle_input):
    """Parse input."""
    matrix = np.genfromtxt(StringIO(puzzle_input), dtype='str', delimiter=1, deletechars=None, comments=None)
    return matrix


def parse_data(puzzle_input):
    pattern = r'(\d+)'
    result = defaultdict(list)
    for idx, row in enumerate(puzzle_input.split('\n')):
        matches = re.finditer(pattern, row)
        for match in matches:
            #print("{}: [{}, ({}, {})]".format(match.group(), idx, match.start(), match.end()))
            result[match.group()].append(idx)
            result[match.group()].append(match.span())

    return result, parse_data_np(puzzle_input)


def find_cells_near_symbol(data):
    symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+', '=']
    mask = np.isin(data, symbols)
    for x, y in zip(*np.where(mask)):
        adj = find_adj(data, x, y)
        for idx, v in enumerate(adj):
            if v != '.':
                print(idx, v, data[x, y])


def has_adjacent(matrix, x_coord, y_coord):
    symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+', '=']

    adjacency = [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if not (i == j == 0)]
    for dx, dy in adjacency:
        if 0 <= (x_coord + dx) < np.shape(matrix)[1] and 0 <= y_coord + dy < np.shape(matrix)[1]:
            cv = matrix[x_coord + dx, y_coord + dy]
            if cv in symbols:
                return True

    return False


def part1(data, matrix):
    """Solve part 1."""

    matches = []
    for k, v in data.items():
        for x in range(v[1][0], v[1][1]):
            if has_adjacent(matrix, v[0], x):
                k_int = int(k)
                if k_int not in matches:
                    matches.append(k_int)

    print(sum(matches))


def part2(data):
    """Solve part 2."""


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data, matrix = parse_data(puzzle_input)
    yield part1(data, matrix)
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
        print("\n".join(str(solution) for solution in solutions))
