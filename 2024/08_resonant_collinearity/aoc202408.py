"""AoC 8, 2024: resonant_collinearity."""

# Standard library imports
import pathlib
import sys
from collections import defaultdict
import itertools
from utils.utils import Point


class Data(object):
    def __init__(self, antenna_map, location_map, size):
        self.size = size
        self.location_map = location_map
        self.antenna_map = antenna_map
        self.antinode_map = []


def parse_data(puzzle_input):
    """Parse input."""
    antenna = defaultdict(list)
    location = defaultdict(list)
    rows = 0
    cols = 0
    for r_idx, row in enumerate(puzzle_input.split('\n')):
        rows += 1
        cols = len(list(row))
        for c_idx, col in enumerate(list(row)):
            point = Point(r_idx, c_idx)
            antenna[col].append(point)
            location[point].append(col)


    return Data(antenna, location, (rows, cols))


def in_grid(size, point):
    return 0 <= point.row < size[0] and 0 <= point.col < size[1]


def part1(data):
    """Solve part 1."""
    print()
    for antenna, locations in data.antenna_map.items():
        if antenna == '.':
            continue
        pairs = list(itertools.combinations(locations, 2))
        for pair in pairs:
            row_offest = abs(pair[0].row - pair[1].row)
            col_offset = abs(pair[0].col - pair[1].col)
            if pair[0].row < pair[1].row:
                antinode1_row = pair[0].row - row_offest
                antinode2_row = pair[1].row + row_offest
            else:
                antinode1_row = pair[0].row - row_offest
                antinode2_row = pair[1].row + row_offest

            if pair[0].col < pair[1].col:
                antinode1_col = pair[0].col - col_offset
                antinode2_col = pair[1].col + col_offset
            else:
                antinode1_col = pair[0].col + col_offset
                antinode2_col = pair[1].col - col_offset

            antinode1 = Point(antinode1_row, antinode1_col)
            antinode2 = Point(antinode2_row, antinode2_col)
            if in_grid(data.size, antinode1):
                if antinode1 not in data.antinode_map:
                    data.antinode_map.append(antinode1)
                    data.location_map[antinode1].append('#')
                    #print(f'Pair {pair[0]}, {pair[1]} has antinode: {antinode1} ({row_offest}, {col_offset})')
            if in_grid(data.size, antinode2):
                if antinode2 not in data.antinode_map:
                    data.antinode_map.append(antinode2)
                    data.location_map[antinode2].append('#')
                    #print(f'Pair {pair[0]}, {pair[1]} has antinode: {antinode2} ({row_offest}, {col_offset})')

    #display(data)

    return len(data.antinode_map)

def part2(data):
    """Solve part 2."""


def display(data):
    print()
    for row in range(data.size[0]):
        row_contents = []
        for col in range(data.size[1]):
            point = Point(row, col)
            row_contents.append(data.location_map.get(point)[-1])
        print(''.join(row_contents))
    print()

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
