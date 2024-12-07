"""AoC 6, 2024: guard_gallivant."""

# Standard library imports
import pathlib
import sys
from collections import defaultdict
from enum import Enum
import re

import numpy as np
import matplotlib.pyplot as plt

class Direction(Enum):
    UP = '^'
    DOWN = 'v'
    RIGHT = '>'
    LEFT = '<'


class Point(object):
    def __init__(self, row, col):
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
        return f'Point({self.row}, {self.col})'

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col


class Guard(object):
    def __init__(self, direction, pos):
        self.direction = direction
        self.pos = pos
        self.goal = None
        self.done = False
        self.history = []

    @property
    def row(self):
        return self.pos.row

    @property
    def col(self):
        return self.pos.col

    def move(self, data):
        if self.direction == Direction.UP:
            self.history.append(move_up(data, self))
        elif self.direction == Direction.DOWN:
            self.history.append(move_down(data, self))
        elif self.direction == Direction.RIGHT:
            self.history.append(move_right(data, self))
        elif self.direction == Direction.LEFT:
            self.history.append(move_left(data, self))

        self.update()

    def update(self):
        self.pos = self.goal
        self.goal = None
        self.turn()

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
        return f'Guard(point={self.pos}, direction-{self.direction}, goal={self.goal})'


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


def move_up(data, guard):
    obstacles = [o for o in data.get('#') if o.col == guard.col and o.row <= guard.row]
    if len(obstacles) == 0:
        guard.goal = Point(0, guard.col)
        guard.done = True
    else:
        row_list = [x.row for x in obstacles]
        closest = min(row_list, key=lambda x: abs(x - guard.row))
        obstacle = [x for x in obstacles if x.row == closest][0]
        guard.goal = Point(obstacle.row + 1, guard.col)

    visited = [Point(x, guard.pos.col) for x in range(guard.pos.row - 1, guard.goal.row - 1, -1)]
    return visited


def move_down(data, guard):
    obstacles = [o for o in data.get('#') if o.col == guard.col and o.row > guard.row]
    if len(obstacles) == 0:
        guard.goal = Point(data.get('size')[0][0] - 1, guard.col)
        guard.done = True
    else:
        row_list = [x.row for x in obstacles]
        closest = min(row_list, key=lambda x: abs(x - guard.row))
        obstacle = [x for x in obstacles if x.row == closest][0]
        guard.goal = Point(obstacle.row - 1, guard.col)

    visited = [Point(x, guard.pos.col) for x in range(guard.pos.row + 1, guard.goal.row + 1)]
    return visited


def move_right(data, guard):
    obstacles = [o for o in data.get('#') if o.row == guard.row and o.col > guard.col]
    if len(obstacles) == 0:
        guard.goal = Point(guard.row, data.get('size')[0][1] - 1)
        guard.done = True
    else:
        col_list = [x.col for x in obstacles]
        closest = min(col_list, key=lambda x: abs(x - guard.col))
        obstacle = [x for x in obstacles if x.col == closest][0]
        guard.goal = Point(guard.row, obstacle.col - 1)

    visited = [Point(guard.pos.row, x) for x in range(guard.pos.col + 1, guard.goal.col + 1)]
    return visited


def move_left(data, guard):
    obstacles = [o for o in data.get('#') if o.row == guard.row and o.col < guard.col]
    if len(obstacles) == 0:
        guard.goal = Point(guard.row, 0)
        guard.done = True
    else:
        col_list = [x.col for x in obstacles]
        closest = min(col_list, key=lambda x: abs(x - guard.col))
        obstacle = [x for x in obstacles if x.col == closest][0]
        guard.goal = Point(guard.row, obstacle.col + 1)

    visited = [Point(guard.pos.row, x) for x in range(guard.pos.col - 1, guard.goal.col - 1, -1)]
    return visited


def display(data, history):
    size = data.get('size')[0]
    grid = np.zeros(size)

    fig, ax = plt.subplots(figsize=(10,10))
    ax.imshow(grid, cmap=plt.cm.terrain)
    line, = ax.plot([],[], color="black")
    plt.ion()
    plt.show()
    for o in data.get('#'):
        plt.gcf().canvas.draw()
        line, = ax.plot(o.row, o.col, '.', c='black')
        #plt.pause(0.1)
    for record in history:
        for point in record:
            plt.gcf().canvas.draw()
            line, = ax.plot(point.row, point.col, '.', c='red')
            plt.pause(0.1)


def part1(data):
    """Solve part 1."""
    visited_locations = []
    guard = data['guard'][0]
    guard.history.append([guard.pos])
    while not guard.done:
        guard.move(data)

    for visited in guard.history:
        for pos in visited:
            if pos not in visited_locations:
                visited_locations.append(pos)

    return len(visited_locations)


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
