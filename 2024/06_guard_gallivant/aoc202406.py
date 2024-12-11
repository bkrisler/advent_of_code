"""AoC 6, 2024: guard_gallivant."""
import collections
import copy
import pathlib
import sys
import typing
from collections import defaultdict
from enum import Enum
import re
import multiprocessing
from multiprocessing import Queue


class Direction(Enum):
    # UP = ('^', lambda p: Point(p.row - 1, p.col))
    # DOWN = ('v', lambda p: Point(p.row + 1, p.col))
    # RIGHT = ('>', lambda p: Point(p.row, p.col + 1))
    # LEFT = ('<', lambda p: Point(p.row, p.col - 1))

    UP = '^'
    DOWN = 'v'
    RIGHT = '>'
    LEFT = '<'

    def __init__(self, key):
        self.key = key
        #self.f = f

    def next(self, pt):
        if self.key == '^':
            return Point(pt.row - 1, pt.col)
        elif self.key == 'v':
            return Point(pt.row + 1, pt.col)
        elif self.key == '>':
            return Point(pt.row, pt.col + 1)
        elif self.key == '<':
            return Point(pt.row, pt.col - 1)


    def __str__(self):
        return f'{self.key}'

class Point(object):
    def __init__(self, row: int, col: int):
        self._row = row
        self._col = col

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, row):
        self._row = row

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, col):
        self._col = col

    def __str__(self):
        return f'Point(row={self._row}, col={self._col})'

    def __repr__(self):
        return f'Point(row={self._row}, col={self._col})'

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self._row, self._col))


class Visited(object):
    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction

    def __str__(self):
        return f'Visited(pos={self.pos}, dir={self.direction.key})'

    def __repr__(self):
        return f'({self.pos}, {self.direction.key})'

    def __eq__(self, other):
        return self.pos == other.pos and self.direction.key == other.direction.key

    def __hash__(self):
        return hash((self.pos, self.direction.key))

class Guard(object):
    def __init__(self, direction: Direction, pos: Point):
        self.direction = direction
        self.pos = pos
        self.done = False
        self.looping = False
        self.history = []

    @property
    def row(self):
        return self.pos.row

    @property
    def col(self):
        return self.pos.col

    def move(self, data: typing.Dict, check: bool=False):
        grid_size = data.get('size')[0]
        new_pos = self.direction.next(self.pos)
        if check:
            self.looping = self.check_loop()
            if self.looping:
                return

        if 0 <= new_pos.row < grid_size[0] and 0 <= new_pos.col < grid_size[1]:
            if new_pos in data.get('#'):
                self.turn()
            else:
                self.history.append(Visited(self.pos, self.direction))
                self.pos = new_pos
        else:
            self.history.append(Visited(self.pos, self.direction))
            self.done = True

    def check_loop(self):
        counts = collections.Counter(self.history)
        if len(counts) > 4 and counts.most_common()[0][1] > 2:
            return True

        return False


    def turn(self):
        if self.direction == Direction.UP:
            self.direction = Direction.RIGHT
        elif self.direction == Direction.RIGHT:
            self.direction = Direction.DOWN
        elif self.direction == Direction.DOWN:
            self.direction = Direction.LEFT
        elif self.direction == Direction.LEFT:
            self.direction = Direction.UP

    def __str__(self):
        return f'Guard(point={self.pos}, direction={self.direction})'


def parse_data(puzzle_input):
    """Parse input."""
    blocks = defaultdict(list)
    rows = len(puzzle_input.split('\n'))
    cols = len(list(puzzle_input.split('\n')[0]))
    blocks['size'].append((rows, cols))
    for idx, row in enumerate(puzzle_input.split('\n')):
        cols = list(row)
        if '^' in cols:
            blocks['guard'].append(Guard(Direction.UP, Point(idx, cols.index('^'))))
        elif '>' in cols:
            blocks['guard'].append(Guard(Direction.RIGHT, Point(idx, cols.index('>'))))
        elif '<' in cols:
            blocks['guard'].append(Guard(Direction.LEFT, Point(idx, cols.index('<'))))
        elif 'v' in cols:
            blocks['guard'].append(Guard(Direction.DOWN, Point(idx, cols.index('v'))))

        p = re.compile('\#')
        blocks['#'].extend([Point(idx, m.start()) for m in re.finditer(p, row)])

    return blocks


def part1(data):
    """Solve part 1."""
    guard = data['guard'][0]
    while not guard.done:
        guard.move(data)

    unique_visited = []
    for visited in guard.history:
        if visited.pos not in unique_visited:
            unique_visited.append(visited.pos)

    return len(unique_visited)


def part2(data):
    """Solve part 2."""
    count = 0
    params = []

    for r_idx in range(data.get('size')[0][0]):
        for c_idx in range(data.get('size')[0][1]):
            guard = Guard(data['guard'][0].direction, data['guard'][0].pos)
            params.append((data, guard, Point(r_idx, c_idx)))

    with multiprocessing.Pool() as pool:
        for result in pool.starmap(process_column, params):
            count += result
    pool.close()

    print(f"Count: {count}")
    return count


def process_column(data, guard, point):
    if point not in data.get('#'):
        dc = copy.deepcopy(data)
        dc['#'].append(point)
        while not guard.done:
            guard.move(dc, True)
            if guard.looping:
                print(f"Valid block point: {dc['#'][-1]}")
                return 1
    return 0


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse_data(puzzle_input)
    #yield part1(data)
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
        print("\n".join(str(solution) for solution in solutions))
