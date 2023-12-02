"""Tests for AoC 1, 2023: Trebuchet."""

# Standard library imports
import pathlib

# Third party imports
import aoc202301
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202301.parse_data_one(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202301.parse_data_two(puzzle_input)

@pytest.fixture
def test1():
    puzzle_input = (PUZZLE_DIR / "test1.txt").read_text().rstrip()
    return aoc202301.parse_data_two(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1[0] == ['1', '2']
    assert len(example1[-1]) == 1


def test_parse_example2(example2):
    """Test that input is parsed properly."""
    assert example2[0] == ['2', '1', '9']
    assert example2[-1] == ['7', '6']


def test_parse_test1(test1):
    """Test that input is parsed properly."""
    assert test1[0] == ['1', '8', '3']
    assert test1[1] == ['4', '1', '8']
    assert test1[2] == ['6', '1', '8', '3']
    assert test1[3] == ['2', '3', '8']
    assert test1[3] == ['2', '3', '8', '2']


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202301.part1(example1) == 142


def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202301.part2(example2) == 281


def test_part2_a(test1):
    """Test part 2 on example input."""
    assert aoc202301.part2(test1) == 174
