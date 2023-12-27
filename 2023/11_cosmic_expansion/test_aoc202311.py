"""Tests for AoC 11, 2023: Cosmic Expansion."""

# Standard library imports
import pathlib

# Third party imports
import aoc202311
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202311.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202311.parse_data(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1
    assert len(example1) == 10
    assert len(example1[0]) == 10


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202311.part1(example1) == 374


@pytest.mark.skip(reason="Not implemented")
def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202311.part2(example1) == 374


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202311.part2(example2) == ...
