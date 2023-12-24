"""AoC 10, 2023: Pipe Maze."""
import itertools
# Standard library imports
import pathlib
import sys
from collections import defaultdict

import numpy as np


def parse_data(puzzle_input):
    """Parse input."""
    grid = []
    for row in puzzle_input.split('\n'):
        grid.append([x for x in row])
    return np.array(grid)


NORTH_SOUTH = '|'
EAST_WEST = '-'
NORTH_EAST = 'L'
NORTH_WEST = 'J'
SOUTH_WEST = '7'
SOUTH_EAST = 'F'
START = 'S'


def get_choices(type, pos, grid):
    all_moves = list(itertools.product([-1, 0, 1], repeat=2))
    all_moves.remove((0, 0))
    choices = np.array(pos) + np.array(all_moves)
    # Remove the impossible
    choices = choices[((choices >= 0) & (choices <= 2)).all(axis=1)]

    if type == START:
        mask = np.array([[0, 1, 0],
                         [1, 0, 1],
                         [0, 1, 0]]).astype(bool)
        res = grid[pos[0] - 1:pos[0] + 2, pos[1] - 1:pos[1] + 2][mask]
        values = []
        for choice in choices:
            v = grid[choice[0]][choice[1]]
            values.append(v)
        print(choices)

    return choices


def get_moves(pos, sz):
    all_moves = list(itertools.product([-1, 0, 1], repeat=2))
    all_moves.remove((0, 0))
    all_moves.remove((-1, -1))
    all_moves.remove((1, 1))
    all_moves.remove((-1, 1))
    all_moves.remove((1, -1))
    choices = np.array(pos) + np.array(all_moves)
    # Remove the impossible
    choices = choices[((choices >= 0) & (choices <= sz)).all(axis=1)]
    return tuple(map(tuple, choices))


def get_value(p, grid):
    return grid[p[0]][p[1]]


def is_valid(src, nxt, orient):
    if src == 'S':
        valid = {'T': ['|', 'F', '7'], 'L': ['-', 'F', 'L'],
                 'R': ['-', 'J', '7'], 'B': ['L', 'J', '|']}
    elif src == '-':
        valid = {'T': [], 'L': ['S', '-', 'F', 'L', 'J', '7'],
                 'R': ['S', '-', 'J', '7', 'L', 'F'], 'B': []}
    elif src == '|':
        valid = {'T': ['S', '|', 'F', '7', 'L', 'J'], 'L': [],
                 'R': [], 'B': ['S', 'F', '7', 'L', 'J', '|']}
    elif src == 'L':
        valid = {'T': ['S', '|', 'F', '7'], 'L': [],
                 'R': ['S', '-', 'J', '7'], 'B': []}
    elif src == 'J':
        valid = {'T': ['S', '|', 'F', '7'], 'L': ['S', '-', 'F', 'L'],
                 'R': [], 'B': []}
    elif src == '7':
        valid = {'T': [], 'L': ['S', '-', 'F', 'L'],
                 'R': [], 'B': ['S', 'L', 'J', '|']}
    elif src == 'F':
        valid = {'T': [], 'L': [],
                 'R': ['S', '-', 'J', '7'], 'B': ['S', 'L', 'J', '|']}
    elif src == 'S':
        return None
    else:
        raise Exception("Error!")

    return nxt in valid[orient]


def get_next(p, grid):
    moves = get_moves(p, len(grid[0]))
    paths = []

    for idx, orient in enumerate(['T', 'L', 'R', 'B']):
        if is_valid(get_value(p, grid), get_value(moves[idx], grid), orient):
            paths.append(moves[idx])

    return paths


def extract_path(grid):
    start = np.where(grid == START)
    crnt = (start[0][0], start[1][0])
    result = defaultdict(list)
    children = get_next(crnt, grid)
    tp = []
    while children is not None:
        tp.append(get_value(crnt, grid))

        x = children[0]
        if x in result.keys():
            x = children[1]

        result[crnt].append(x)

        children = get_next(x, grid)
        if (start[0][0], start[1][0]) in children and crnt != (start[0][0], start[1][0]):
            result[x].append((start[0][0], start[1][0]))
            tp.append(get_value(x, grid))
            children = None

        crnt = x

    length = len(result.keys()) / 2.0
    return length


def part1(data):
    """Solve part 1."""
    result = extract_path(data)
    return int(result)


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
