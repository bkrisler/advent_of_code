"""Tests for AoC 6, 2024: guard_gallivant."""

# Standard library imports
import pathlib

# Third party imports
import aoc202406
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202406.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202406.parse_data(puzzle_input)

@pytest.fixture
def example3():
    puzzle_input = (PUZZLE_DIR / "example3.txt").read_text().rstrip()
    return aoc202406.parse_data(puzzle_input)


@pytest.fixture
def example4():
    puzzle_input = (PUZZLE_DIR / "example4.txt").read_text().rstrip()
    return aoc202406.parse_data(puzzle_input)

@pytest.fixture
def example5():
    puzzle_input = (PUZZLE_DIR / "example5.txt").read_text().rstrip()
    return aoc202406.parse_data(puzzle_input)

@pytest.fixture
def example6():
    puzzle_input = (PUZZLE_DIR / "example6.txt").read_text().rstrip()
    return aoc202406.parse_data(puzzle_input)

#@pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 is not None
    assert '#' in example1
    assert 'guard' in example1

#@pytest.mark.skip(reason="Not implemented")
def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202406.part1(example1) == 41


def test_part1_example3(example3):
    """Test part 1 on example input."""
    assert aoc202406.part1(example3) == 44


def test_part1_example4(example4):
    """Test part 1 on example input."""
    assert aoc202406.part1(example4) == 7

def test_part1_example5(example5):
    """Test part 1 on example input."""
    assert aoc202406.part1(example5) == 23

def test_part1_example6(example6):
    """Test part 1 on example input."""
    assert aoc202406.part1(example6) == 11

@pytest.mark.skip(reason="Not implemented")
def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202406.part2(example1) == ...


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202406.part2(example2) == ...
