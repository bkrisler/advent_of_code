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


def test_rank_p2():
    assert sorted(['Q2Q2Q', 'JJJJ2', '2JJJJ', '2AAAA'], key=aoc202307.find_type_two) == ['Q2Q2Q', '2AAAA', 'JJJJ2', '2JJJJ']


def test_full_house():
    inn = ['2233J', '22334']
    out = ['22334', '2233J']
    assert aoc202307.rank_sort_p2(inn) == out

    inn = ['2233J', 'QQKJK']
    out = ['2233J', 'QQKJK']
    assert aoc202307.rank_sort_p2(inn) == out

    inn = ['JJJ34', 'QQKJK']
    out = ['QQKJK', 'JJJ34']
    assert aoc202307.rank_sort_p2(inn) == out

    inn = ['2345J', 'QQKJK']
    out = ['2345J', 'QQKJK']
    assert aoc202307.rank_sort_p2(inn) == out

    inn = ['4T48J', 'QQKJK']
    out = ['4T48J', 'QQKJK']
    assert aoc202307.rank_sort_p2(inn) == out

    inn = ['4T48J', 'JJJJJ']
    out = ['4T48J', 'JJJJJ']
    assert aoc202307.rank_sort_p2(inn) == out


def test_second_order_p2():
    assert aoc202307.second_order_p2('23456', '23457') == -1
    assert aoc202307.second_order_p2('23457', '23456') == 1
    assert aoc202307.second_order_p2('J2345', 'J3426') == -1
    assert aoc202307.second_order_p2('AAAAQ', 'AAAAT') == 1
    assert aoc202307.second_order_p2('JJJJJ', 'QQQQQ') == -1
    assert aoc202307.second_order_p2('2345J', '23455') == -1


def test_rank_sort_p2():
    assert aoc202307.rank_sort_p2(['AAAAA', 'JJJJJ']) == ['JJJJJ', 'AAAAA']
    assert aoc202307.rank_sort_p2(['AAAAA', 'JJJJJ', '55555']) == ['JJJJJ', '55555', 'AAAAA']
    inn = ['23456', 'AAAAA', 'JJJJJ', '2345J', '22345', '4J499', '44355', '667JJ', '55566', '44J9J']
    out = ['23456', '22345', '2345J', '44355', '4J499', '55566', '44J9J', '667JJ', 'JJJJJ', 'AAAAA']
    assert aoc202307.rank_sort_p2(inn) == out
    assert aoc202307.rank_sort_p2(['23458', '8642A']) == ['23458', '8642A']
    inn = ['8888J', 'AAAAJ', 'J345J', '44556', '23456', 'J4J55', 'J3456']
    out = ['23456', 'J3456', '44556', 'J345J', 'J4J55', '8888J', 'AAAAJ']
    assert aoc202307.rank_sort_p2(inn) == out
    assert aoc202307.rank_sort_p2(['98765', 'J2345']) == ['98765', 'J2345']
    assert aoc202307.rank_sort_p2(['JJ987', 'JJ98J']) == ['JJ987', 'JJ98J']


@pytest.mark.skip(reason="Not implemented")
def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202307.part2(example1) == ...


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202307.part2(example2) == ...
