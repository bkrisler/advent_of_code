"""Tests for AoC 3, 2022: rucksack."""

# Standard library imports
import pathlib

# Third party imports
import aoc202203
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().strip()
    return aoc202203.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().strip()
    return aoc202203.parse_data(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert len(example1) == 6
    assert example1[0] == ['v', 'J', 'r', 'w', 'p', 'W', 't', 'w', 'J', 'g', 'W', 'r', 'h', 'c', 's', 'F', 'M', 'M', 'f', 'F', 'F', 'h', 'F', 'p']
    assert example1[-1] == ['C', 'r', 'Z', 's', 'J', 's', 'P', 'P', 'Z', 's', 'G', 'z', 'w', 'w', 's', 'L', 'w', 'L', 'm', 'p', 'w', 'M', 'D', 'w']


@pytest.mark.parametrize("data,expected",
                         [(['A', 'B', 'C', 'A'], ['A']),
                          (['A', 'B', 'C', 'b', 'C'], ['C'])
                          ])
def test_find_duplicates(data, expected):
    assert aoc202203.find_duplicates(data) == expected


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202203.part1(example1) is 157


def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202203.part2(example1) == 70


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202203.part2(example2) == ...
