"""AoC 6, 2024: guard_gallivant."""

# Standard library imports
import pathlib
import sys
import typing
from collections import defaultdict
from enum import Enum
import re


class Direction(Enum):
    UP = ('^', lambda p: Point(p.row - 1, p.col))
    DOWN = ('v', lambda p: Point(p.row + 1, p.col))
    RIGHT = ('>', lambda p: Point(p.row, p.col + 1))
    LEFT = ('<', lambda p: Point(p.row, p.col - 1))

    def __init__(self, key, f):
        self.key = key
        self.f = f

    def next(self, pt):
        return self.f(pt)

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

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col


class Visited(object):
    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction

    def __str__(self):
        return f'Visited(pos={self.pos}, dir={self.direction.key})'

class Guard(object):
    def __init__(self, direction: Direction, pos: Point):
        self.direction = direction
        self.pos = pos
        self.goal = None
        self.done = False
        self.history = []
        self.safe_blocks = []

    @property
    def row(self):
        return self.pos.row

    @property
    def col(self):
        return self.pos.col

    def move(self, data: typing.Dict, loop_check: bool=False):
        grid_size = data.get('size')[0]
        new_pos = self.direction.next(self.pos)
        if new_pos.row >= 0 and new_pos.col >= 0 and new_pos.row < grid_size[0] and new_pos.row < grid_size[1]:
            if new_pos in data.get('#'):
                self.turn()
            else:
                self.history.append(Visited(self.pos, self.direction))
                self.pos = new_pos
                if loop_check:
                    self.check_loop(data.get('#'))

        else:
            self.history.append(Visited(self.pos, self.direction))
            self.done = True

    def check_loop(self, blockers):
        if self.direction == Direction.UP:
            row_history = [v for v in self.history if v.pos.row == self.row
                           and (v.direction == Direction.RIGHT or v.direction == Direction.LEFT) ]
            if len(row_history) > 0:
                one_right = Point(self.row, self.col + 1)
                if one_right in [v.pos for v in row_history]:
                    self.safe_blocks.append(Point(self.row - 1, self.col))
                else:
                    row_blocks = [b for b in blockers if b.row == self.row]
                    blocker = [b for b in row_blocks if b.row < self.row]
                    if len(blocker) > 0:
                        visited_cols = [x.pos.col for x in row_history]
                        if self.col > max(visited_cols):
                            self.safe_blocks.append(Point(self.row - 1, self.col))
        elif self.direction == Direction.RIGHT:
            col_history = [v for v in self.history if v.pos.col == self.col
                           and (v.direction == Direction.UP or v.direction == Direction.DOWN)]
            if len(col_history) > 0:
                one_down = Point(self.row + 1, self.col)
                if one_down in [v.pos for v in col_history]:
                    self.safe_blocks.append(Point(self.row, self.col + 1))
                else:
                    col_blocks = [b for b in blockers if b.col == self.col]
                    blocker = [b for b in col_blocks if b.row > self.row]
                    if len(blocker) > 0:
                        visited_rows = [x.pos.row for x in col_history]
                        if self.row < min(visited_rows):
                            self.safe_blocks.append(Point(self.row, self.col + 1))
        elif self.direction == Direction.DOWN:
            row_history = [v for v in self.history if v.pos.row == self.row
                           and (v.direction == Direction.RIGHT or v.direction == Direction.LEFT) ]
            if len(row_history) > 0:
                one_left = Point(self.row, self.col - 1)
                if one_left in [v.pos for v in row_history]:
                    self.safe_blocks.append(Point(self.row + 1, self.col))
                else:
                    row_blocks = [b for b in blockers if b.row == self.row]
                    blocker = [b for b in row_blocks if b.row < self.row]
                    if len(blocker) > 0:
                        visited_cols = [x.pos.col for x in row_history]
                        if self.col < min(visited_cols):
                            self.safe_blocks.append(Point(self.row + 1, self.col))
        elif self.direction == Direction.LEFT:
            col_history = [v for v in self.history if v.pos.col == self.col
                           and (v.direction == Direction.UP or v.direction == Direction.DOWN)]
            if len(col_history) > 0:
                one_up = Point(self.row - 1, self.col)
                if one_up in [v.pos for v in col_history]:
                    self.safe_blocks.append(Point(self.row, self.col - 1))
                else:
                    col_blocks = [b for b in blockers if b.col == self.col]
                    blocker = [b for b in col_blocks if b.row < self.row]
                    if len(blocker) > 0:
                        visited_rows = [x.pos.row for x in col_history]
                        if self.row > max(visited_rows):
                            self.safe_blocks.append(Point(self.row, self.col + 1))

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


def path_right(history: typing.List, point: Point) -> bool:
    target_row = point.row
    for visited in history:
        for pos in visited:
            if pos.row == target_row and pos.col > point.col:
                return True

    return False

def path_left(history: typing.List, point: Point) -> bool:
    target_row = point.row
    for visited in history:
        for pos in visited:
            if pos.row == target_row and pos.col < point.col:
                return True

    return False

def path_up(history: typing.List, point: Point) -> bool:
    target_col = point.col
    for visited in history:
        for pos in visited:
            if pos.col == target_col and pos.col < point.col:
                return True

    return False

def path_down(history: typing.List, point: Point) -> bool:
    target_col = point.col
    for visited in history:
        for pos in visited:
            if pos.col == target_col and pos.col > point.col:
                return True

    return False

def check_history(guard: Guard, visited: typing.List, direction: Direction):
    for point in visited:
        print(f"Point: {point} and Guard: {guard.pos}")
        if guard.pos.row == point.row and guard.pos.col == point.col:
            print("HERE")
    print("Not Here")

    return None


def part1(data):
    """Solve part 1."""
    guard = data['guard'][0]
    while not guard.done:
        guard.move(data, loop_check=True)

    unique_visited = []
    for visited in guard.history:
        if visited.pos not in unique_visited:
            unique_visited.append(visited.pos)

    return len(unique_visited)


def part2(data):
    """Solve part 2."""
    print()

    guard = data['guard'][0]
    while not guard.done:
        guard.move(data, loop_check=True)

    return len(guard.safe_blocks)


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
