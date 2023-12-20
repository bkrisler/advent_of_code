"""AoC 7, 2023: Camel Cards."""
import functools
# Standard library imports
import pathlib
import re
import sys

from collections import Counter


def parse_data(puzzle_input):
    """Parse input."""
    result = []
    for row in puzzle_input.split("\n"):
        res = re.findall(r"(.*)\s(\d+)", row)
        result.append(res[0])
    return result


def find_type(hand):
    res = Counter(hand)
    if 5 in res.values():
        return 18
    elif 4 in res.values():
        return 15
    elif 3 in res.values() and 2 in res.values():
        return 12
    elif 3 in res.values():
        return 9
    elif len([x for x in res.values() if x == 2]) == 2:
        return 6
    elif len([x for x in res.values() if x == 2]) == 1:
        return 3

    return 0


def get_higher(a, b):
    ranking = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2', '1']
    if ranking.index(a) < ranking.index(b):
        return a
    else:
        return b


def second_order(hand1, hand2):
    t1 = find_type(hand1)
    t2 = find_type(hand2)
    result = 0
    if t1 == t2:
        for x in range(5):
            if hand1[x] != hand2[x]:
                higher = get_higher(hand1[x], hand2[x])
                if hand1[x] == higher:
                    result = 1
                    break
                else:
                    result = -1
                    break
    else:
        result = 0

    #print("Compare: {} with {} == {}".format(hand1, hand2, result))
    return result


def rank_sort(hand):
    phase_1 = sorted(hand, key=find_type)
    phase_2= sorted(phase_1, key=functools.cmp_to_key(second_order))
    return phase_2


def part1(data):
    """Solve part 1."""
    hand = [x[0] for x in data]
    bids = dict(data)
    ranked = rank_sort(hand)
    winnings = 0
    for idx, hand in enumerate(ranked, 1):
        bid = int(bids[hand]) * idx
        #print("{} has rank {} and bid: {}".format(hand, idx, bid))
        winnings += bid

    return winnings


def part2(data):
    """Solve part 2."""


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
