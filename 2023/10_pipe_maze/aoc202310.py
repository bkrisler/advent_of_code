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


def get_neighbors(pos, sz):
    n_idx = list(itertools.product([-1, 0, 1], repeat=2))
    n_idx.remove((0, 0))
    neighbors = np.array(pos) + np.array(n_idx)
    neighbors = neighbors[((neighbors >= 0) & (neighbors <= sz)).all(axis=1)]
    return tuple(map(tuple, neighbors))


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
    start = np.where(grid == 'S')
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

    return result


def poly_area(fpath):
    points = list(fpath.keys())
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def internal_points(area, edge_points):
    return (2 * area - edge_points + 2) / 2


def brute_find(fpath, sz):
    all_points = list(fpath.keys())
    grid = np.zeros(sz)
    for p in all_points:
        grid[p[0]][p[1]] = 1

    # Trim empty rows and cols
    mask = grid == 0
    empty_rows = np.flatnonzero((~mask).sum(axis=1))
    empty_cols = np.flatnonzero((~mask).sum(axis=0))
    grid = grid[empty_rows.min():empty_rows.max()+1, empty_cols.min():empty_cols.max()+1]
    ones = np.transpose(np.where(grid == 1))
    # for point in ones:
    #     neighbors = get_neighbors(point, sz)
    #     for n in neighbors:
    #         nn = (int(n[0]), int(n[1]))
    #         try:
    #             v = get_value(nn, grid)
    #             if v == 0:
    #                 grid[nn[0], nn[1]] = 2
    #         except IndexError:
    #             pass

    np.savetxt('dump3.txt', grid.astype(int), fmt='%i', delimiter='')

    contained = 0
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row][col] == 0:
                left = grid[0:col, row]
                right = grid[col+1:, row]
                top = grid[col, 0:row]
                bottom = grid[col, row+1:]
                if 1 in left and 1 in right and 1 in top and 1 in bottom:
                    contained += 1
                    print("{}, {} = {}".format(row, col, grid[row][col]))
                #print("{} and {}".format(len(left), len(right)))

    return contained

    # twos = np.transpose(np.where(grid == 2))
    # for point in twos:
    #     neighbors = get_neighbors(point, sz)
    #     for n in neighbors:
    #         nn = (int(n[0]), int(n[1]))
    #         try:
    #             v = get_value(nn, grid)
    #             if v == 0:
    #                 grid[nn[0], nn[1]] = 3
    #         except IndexError:
    #             pass



def visualize(fpath, sz):
    all_points = list(fpath.keys())
    grid = np.zeros((sz[0], sz[1]))
    for p in all_points:
        grid[p[0]][p[1]] = 1
    print(grid.shape)
    print()
    mask = grid == 0
    empty_rows = np.flatnonzero((~mask).sum(axis=1))
    empty_cols = np.flatnonzero((~mask).sum(axis=0))
    g2 = grid[empty_rows.min():empty_rows.max()+1, empty_cols.min():empty_cols.max()+1]
    print(g2)

    #print(g2.shape)
    np.savetxt('dump.txt', grid.astype(int), fmt='%i', delimiter='')


def part1(data):
    """Solve part 1."""
    full_path = extract_path(data)
    #visualize(full_path, data.shape)
    return len(full_path.keys()) / 2.0


def part2(data):
    """Solve part 2."""
    full_path = extract_path(data)
    area = poly_area(full_path)
    result = internal_points(area, len(full_path.keys()))
    return result



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
