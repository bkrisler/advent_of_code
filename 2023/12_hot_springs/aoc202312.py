"""AoC 12, 2023: Hot Springs."""
import itertools
# Standard library imports
import pathlib
import re
import sys
from collections import Counter
from itertools import groupby
from math import factorial


def parse_data(puzzle_input):
    """Parse input."""
    result = []
    for row in puzzle_input.split('\n'):
        matches = re.finditer(r"(.+) (.+)", row)
        for match in matches:
            p1 = match.group(1)
            p2 = [int(x) for x in match.group(2).split(',')]
            result.append([p1, p2])

    return result


def p1_old(data):
    for row in data:
        # groups = ''.join(row[0]).split('.')
        slots = [(x, len(list(y))) for x, y in groupby(row[0]) if x != '.']
        vals = row[1]
        for v in vals:
            if v in [x[1] for x in slots if x[0] == '#']:
                vals.remove(v)
                slots.remove(('#', v))
                break

        result = []
        for slot in slots:
            n = slot[1]
            r = len(vals) - 1
            n = n - r
            for k in vals:
                cnk = factorial(n) / (factorial(n - k) * factorial(k))
                result.append(cnk)
                print()
        print()


def match(records, nums):
    return nums == [sum(1 for _ in grouper)
                    for key, grouper in itertools.groupby(records)
                    if key == '#'
                    ]


def bf(records, nums):
    gen = ('#.' if r == '?' else r for r in records)
    return sum(match(candidate, nums) for candidate in itertools.product(*gen))


def part1(data):
    """Solve part 1.
    """
    result = 0
    for row in data:
        result += bf(row[0], row[1])

    return result


def part2(data):
    """Solve part 2."""
    result = 0
    for row in data:
        result1 = bf(row[0], row[1])
        result2 = bf(row[0]+'?', row[1])
        final = (result2 * 4) * result1
        print()
        # new_row = '' + row[0]
        # new_nums = [x for x in row[1]]
        #
        # for x in range(5):
        #     new_row += '?'
        #     new_row += row[0]
        #     for x in row[1]:
        #         new_nums.append(x)
        #
        # result += bf(new_row, new_nums)

    return result


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse_data(puzzle_input)
    yield part1(data)
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
        print("\n".join(str(solution) for solution in solutions))
