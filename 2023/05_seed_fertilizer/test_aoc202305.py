"""Tests for AoC 5, 2023: Seed Fertilizer."""

# Standard library imports
import pathlib

# Third party imports
import aoc202305
import pytest

from aoc202305 import Range, Row

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202305.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202305.parse_data(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert len(example1.keys()) == 8
    assert example1['seeds'] == ['79', '14', '55', '13']


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202305.part1(example1) == 35


def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202305.part2(example1) == 46


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202305.part2(example2) == ...


def test_row():
    row1 = [4, 9, 3]
    row = Row(row1)
    assert row.get_src().start() == 9
    assert row.get_dest().start() == 4
    assert row.get_dest().end() == 6


def test_row_src_contains():
    row1 = [4, 9, 3]
    row = Row(row1)
    assert row.src_contains(Range(10, 2))
    assert row.src_contains(Range(9, 0))
    assert row.src_contains(Range(11, 0))

    row2 = Row([1, 0, 400])
    assert row2.src_contains(Range(5, 15))

    row3 = Row([1, 0, 4000000000])
    assert row3.src_contains(Range(5000, 15000))


def test_row_dest_range1():
    row = Row([1, 9, 9])
    tr = row.dest_range(Range(11, 2))
    assert tr.start() == 3
    assert tr.end() == 4


def test_row_dest_range2():
    row = Row([1, 9, 9])
    tr = row.dest_range(Range(9, 9))
    assert tr.start() == 1
    assert tr.end() == 9


def test_row_dest_range3():
    row = Row([1, 9, 9])
    tr = row.dest_range(Range(9, 0))
    assert tr.start() == 1
    assert tr.end() == 1


def test_row_dest_range4():
    row = Row([1, 9, 9])
    tr = row.dest_range(Range(9, 1))
    assert tr.start() == 1
    assert tr.end() == 1


def test_row_dest_range5():
    row = Row([1, 9, 9])
    tr = row.dest_range(Range(17, 1))
    assert tr.start() == 9
    assert tr.end() == 9


def test_row_dest_range6():
    row = Row([1, 9, 9])
    tr = row.dest_range(Range(14, 4))
    assert tr.start() == 6
    assert tr.end() == 9


def test_dest_for_tgt():
    row = Row([1, 9, 9])
    dest = row.dest_for_src(Range(14, 4))
    assert dest.start() == 6
    assert dest.end() == 9


def test_overlaps():
    row = Row([1, 9, 9])
    assert row.overlaps(Range(3, 8))


def test_overlaps2():
    row = Row([5, 10, 5])
    # 10 ---- 14
    assert row.overlaps(Range(8, 3))
    assert row.overlaps(Range(8, 14))
    assert row.overlaps(Range(8, 24))
    assert row.overlaps(Range(11, 24))
    assert row.overlaps(Range(14, 2))
    assert row.overlaps(Range(13, 2))

    assert not row.overlaps(Range(8, 2))
    assert not row.overlaps(Range(24, 2))
    assert not row.overlaps(Range(15, 2))


def test_outside():
    row = Row([5, 10, 5])
    # 10 ---- 14
    assert row.outside(Range(3,2))
    assert row.outside(Range(8,2))
    assert row.outside(Range(15,10))

    assert not row.outside(Range(8, 3))
    assert not row.outside(Range(8, 14))
    assert not row.outside(Range(8, 24))
    assert not row.outside(Range(11, 24))
    assert not row.outside(Range(14, 2))
    assert not row.outside(Range(13, 2))


def test_overlapped():
    # D:  5  6  7  8  9
    # S: 10 11 12 13 14
    row = Row([5, 10, 5])
    assert row.overlapped(Range(8, 3)) == [Range(8, 2), Range(10, 1)]
    assert row.overlapped(Range(12, 5)) == [Range(7, 3), Range(15, 2)]
    assert row.overlapped(Range(10, 50)) == [Range(5, 5), Range(10, 45)]
    assert row.overlapped(Range(1, 14)) == [Range(1, 9), Range(10, 5)]


def test_dest_for_src():
    # D:  5  6  7  8  9
    # S: 10 11 12 13 14
    row = Row([5, 10, 5])

    # Test Contained
    assert row.dest_for_src(Range(10, 2)) == [Range(5, 2)]
    assert row.dest_for_src(Range(13, 2)) == [Range(8, 2)]
    assert row.dest_for_src(Range(10, 5)) == [Range(5, 5)]

    # Test Overlap
    assert row.dest_for_src(Range(8, 3)) == [Range(8, 2), Range(10, 1)]
    row2 = Row([100, 0, 20])
    assert row2.dest_for_src(Range(0, 5)) == [Range(100, 5)]

    # Test Outside
    assert row.dest_for_src(Range(8, 2)) == [Range(8, 2)]
    assert row.dest_for_src(Range(800, 200)) == [Range(800, 200)]


def test_range():
    r1 = Range(1, 7)
    assert r1.start() == 1
    assert r1.end() == 7
    assert r1.extent() == 7


def test_range1():
    r = Range(1, 0)
    assert r.start() == 1
    assert r.end() == 1


def test_range2():
    r = Range(1, 1)
    assert r.start() == 1
    assert r.end() == 1


def test_range_create():
    r = Range.create((4, 5))
    assert r.start() == 4
    assert r.end() == 8


def test_from_row():
    row = [4, 5, 3]
    src, dest = Range.from_row(row)
    assert src.start() == 5
    assert src.end() == 7
    assert dest.start() == 4
    assert dest.end() == 6


def test_range_contains():
    r1 = Range(3, 17)
    assert r1.contains(Range(4, 3))
    assert r1.contains(Range(3, 0))
    assert r1.contains(Range(r1.end(), 0))


def test_range_end():
    assert aoc202305.range_end((1, 2)) == 2
    assert aoc202305.range_end((1, 6)) == 6
    assert aoc202305.range_end((20, 22)) == 41


def test_src_range():
    assert aoc202305.src_range([1, 2, 3]) == (2, 3)


def test_dest_range():
    assert aoc202305.dest_range([1, 2, 3]) == (1, 3)


def test_contains():
    assert aoc202305.contains([0, 1, 6], [3, 2])
    #assert aoc202305.contains([1, 6], [1, 1]) == True
    # assert aoc202305.contains([1, 2, 3, 4, 5, 6], [6, 1]) == True
    #assert aoc202305.contains([1, 2, 3, 4, 5, 6], [1, 6]) == True

