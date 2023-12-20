"""Tests for AoC 7, 2023: Camel Cards."""

# Standard library imports
import pathlib

# Third party imports
import aoc202307
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202307.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202307.parse_data(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 is not None
    assert example1[0][0] == '32T3K'
    assert example1[-1][0] == 'QQQJA'


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202307.part1(example1) == None


def test_type_five_of_a_kind():
    assert aoc202307.find_type('AAAAA') == 7
    assert aoc202307.find_type('66666') == 7


def test_type_four_of_a_kind():
    assert aoc202307.find_type('A5AAA') == 6
    assert aoc202307.find_type('68666') == 6


def test_type_full_house():
    assert aoc202307.find_type('AAA55') == 5
    assert aoc202307.find_type('77733') == 5
    assert aoc202307.find_type('JJJ78') == 4


def test_three_of_a_kind():
    assert aoc202307.find_type('44495') == 4
    assert aoc202307.find_type('77733') == 5


def test_two_pair():
    assert aoc202307.find_type('22334') == 3
    assert aoc202307.find_type('AJA4J') == 3


def test_one_pair():
    assert aoc202307.find_type('45468') == 2
    assert aoc202307.find_type('J456J') == 2


def test_high_card():
    assert aoc202307.find_type('34567') == 1
    assert aoc202307.find_type('AKQJ45') == 1


def test_get_higher():
    assert aoc202307.get_higher('A', '8') == 'A'
    assert aoc202307.get_higher('A', 'K') == 'A'
    assert aoc202307.get_higher('2', '1') == '2'
    assert aoc202307.get_higher('1', 'A') == 'A'


def test_second_order():
    assert aoc202307.second_order('A4433', 'A3322') == 'A4433'
    assert aoc202307.second_order('33332', '2AAAA') == '33332'
    assert aoc202307.second_order('77888', '77788') == '77888'


@pytest.mark.skip(reason="Not implemented")
def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202307.part2(example1) == ...


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202307.part2(example2) == ...
