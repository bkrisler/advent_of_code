"""Tests for AoC 4, 2023: Scratchcards."""

# Standard library imports
import pathlib

# Third party imports
import aoc202304
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202304.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202304.parse_data(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1['1'][0] == ['41', '48', '83', '86', '17']


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202304.part1(example1) == 13


def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202304.part2(example1) == 30


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202304.part2(example2) == ...
