"""Tests for AoC 10, 2023: Pipe Maze."""

# Standard library imports
import pathlib

# Third party imports
import aoc202310
import pytest
import numpy as np

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202310.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202310.parse_data(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 is not None
    assert np.shape(example1) == (5, 5)


def test_get_moves():
    grid = [['A', 'B', 'C', 'D'],
          ['E', 'F', 'G', 'H'],
          ['I', 'J', 'K', 'L'],
          ['M', 'N', 'O', 'P']]

    choices = aoc202310.get_moves([1, 1], 3)
    v = [grid[c[0]][c[1]] for c in choices]
    assert grid[1][1] == 'F'
    assert v == ['B', 'E', 'G', 'J']

    choices = aoc202310.get_moves([0, 0], 3)
    v = [grid[c[0]][c[1]] for c in choices]
    assert grid[0][0] == 'A'
    assert v == ['B', 'E']

    choices = aoc202310.get_moves([0, 1], 3)
    v = [grid[c[0]][c[1]] for c in choices]
    assert grid[0][1] == 'B'
    assert v == ['A', 'C', 'F']

    choices = aoc202310.get_moves([3, 0], 3)
    v = [grid[c[0]][c[1]] for c in choices]
    assert grid[3][0] == 'M'
    assert v == ['I', 'N']

    choices = aoc202310.get_moves([2, 1], 3)
    v = [grid[c[0]][c[1]] for c in choices]
    assert grid[2][1] == 'J'
    assert v == ['F', 'I', 'K', 'N']

    choices = aoc202310.get_moves([0, 3], 3)
    v = [grid[c[0]][c[1]] for c in choices]
    assert grid[0][3] == 'D'
    assert v == ['C', 'H']

    choices = aoc202310.get_moves([3, 3], 3)
    v = [grid[c[0]][c[1]] for c in choices]
    assert grid[3][3] == 'P'
    assert v == ['L', 'O']


def test_get_next(example1):
    s = np.where(example1 == 'S')
    nxt = aoc202310.get_next([s[0][0], s[1][0]], example1)
    assert np.array_equal(nxt, [(1, 2), (2, 1)])

    nxt = aoc202310.get_next([1, 2], example1)
    assert np.array_equal(nxt, [(1, 3)])

    nxt = aoc202310.get_next([1, 3], example1)
    assert np.array_equal(nxt, [(1, 2), (2, 3)])


def test_is_valid():
    assert aoc202310.is_valid('S', 'F', 'T')
    assert aoc202310.is_valid('S', '-', 'R')
    assert aoc202310.is_valid('S', '-', 'L')
    assert aoc202310.is_valid('S', '|', 'B')
    assert aoc202310.is_valid('S', '|', 'T')
    assert aoc202310.is_valid('S', 'J', 'R')


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202310.part1(example1) == 4


@pytest.mark.skip(reason="Not implemented")
def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202310.part2(example1) == ...


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202310.part2(example2) == ...
