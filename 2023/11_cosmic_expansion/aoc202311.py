"""AoC 11, 2023: Cosmic Expansion."""
import itertools
# Standard library imports
import pathlib
import sys
import numpy as np


def parse_data(puzzle_input):
    """Parse input."""
    result = []
    for row in puzzle_input.split('\n'):
        result.append([x for x in row])
    return result


def part1(data):
    """Solve part 1."""
    d = np.asarray(data)
    rows = np.where((d == '.').all(axis=1))
    for n in reversed(rows[0]):
        d = np.insert(d, n, np.repeat('.', d.shape[1]), axis=0)

    cols = np.where((d == '.').all(axis=0))
    for n in reversed(cols[0]):
        d = np.insert(d, n, np.repeat('.', d.shape[0]), axis=1)

    galaxies = number_galaxies(d)

    pairs = list(itertools.combinations(galaxies.keys(), 2))
    result = 0
    for pair in pairs:
        start = galaxies[pair[0]]
        end = galaxies[pair[1]]
        result += manhattan_distance(start, end)

    return result


def manhattan_distance(start, end):
    sx, sy = start
    ex, ey = end
    dx = abs(sx - ex)  # Horizontal distance
    dy = abs(sy - ey)  # Vertical distance
    return abs(dx + dy)


def number_galaxies(x):
    galaxies = list(zip(*np.where(x == '#')))
    result = {}
    for idx, g in enumerate(galaxies):
        result[idx] = g
    return result


def part2(data):
    """Solve part 2."""
    d = np.asarray(data)
    rows = np.where((d == '.').all(axis=1))[0]
    cols = np.where((d == '.').all(axis=0))[0]

    galaxies = number_galaxies(d)

    multiplier = 1000000
    multiplier = multiplier - 1

    pairs = list(itertools.combinations(galaxies.keys(), 2))
    result = 0
    for pair in pairs:
        start = list(galaxies[pair[0]])
        end = list(galaxies[pair[1]])

        srm = 0
        erm = 0
        for row in rows:
            if start[0] < row < end[0]:
                erm += multiplier
            if row < start[0]:
                srm += multiplier
                if row < end[0]:
                    erm += multiplier

        start[0] += srm
        end[0] += erm

        scm = 0
        ecm = 0
        for col in cols:
            if col < start[1]:
                scm += multiplier
                if col < end[1]:
                    ecm += multiplier
            elif start[1] < col < end[1]:
                ecm += multiplier

        start[1] += scm
        end[1] += ecm

        r = manhattan_distance(start, end)
        #print("{} to {} is {}".format(start, end, r))
        result += r

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
