"""Tests for AoC 2, 2023: Cube Conundrum."""

# Standard library imports
import pathlib

# Third party imports
import aoc202302
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202302.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202302.parse_data(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert len(example1[1]) == 3


def test_part1_example1(example1):
    """Test part 1 on example input."""
    goal = {'red': 12, 'green': 13, 'blue': 14}
    assert aoc202302.part1(example1, goal) == 8


@pytest.mark.skip(reason="Not implemented")
def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202302.part2(example1) == ...


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202302.part2(example2) == ...
