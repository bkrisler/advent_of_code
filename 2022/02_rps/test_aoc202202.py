"""Tests for AoC 2, 2022: rps."""

# Standard library imports
import pathlib

# Third party imports
import aoc202202
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().strip()
    return aoc202202.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().strip()
    return aoc202202.parse_data(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == [('A', 'Y'), ('B', 'X'), ('C', 'Z')]


@pytest.mark.parametrize("move,expected",
                         [(('A', 'Y'), 4), (('B', 'X'), 1), (('C', 'Z'), 7)])
def test_select_and_play(move, expected):
    assert aoc202202.select_and_play(move) == expected


@pytest.mark.parametrize("move,expected",
                         [(('A', 'Y'), 'X'), (('B', 'X'), 'X'), (('C', 'Z'), 'X')])
def test_select_required_play(move, expected):
    assert aoc202202.select_required_play(move) == expected


@pytest.mark.parametrize("move,expected",
                         [(('A', 'Y'), 8), (('B', 'X'), 1), (('C', 'Z'), 6)])
def test_score_round(move, expected):
    assert aoc202202.score_round(move) == expected


@pytest.mark.parametrize("move,expected",
                         [('A', 'R'), ('B', 'P'), ('C', 'S'), ('X', 'R'), ('Y', 'P'), ('Z', 'S')])
def test_lookup(move, expected):
    assert aoc202202.map_move(move) == expected


@pytest.mark.parametrize("move,expected",
                         [(('A', 'X'), 'T'), (('A', 'Y'), 'W'), (('A', 'Z'), 'L'),
                          (('B', 'X'), 'L'), (('B', 'Y'), 'T'), (('B', 'Z'), 'W'),
                          (('C', 'X'), 'W'), (('C', 'Y'), 'L'), (('C', 'Z'), 'T')])
def test_determine_win(move, expected):
    assert aoc202202.determine_win(move) is expected


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202202.part1(example1) == 15


@pytest.mark.skip(reason="Not implemented")
def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202202.part2(example1) == ...


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202202.part2(example2) == ...
