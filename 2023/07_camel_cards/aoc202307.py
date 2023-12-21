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


def find_type_two(hand):
    result = 0

    res = Counter(hand)
    if 5 in res.values():
        # Five of a kind
        result = 6
    elif 4 in res.values():
        # Four of a kind
        if 'J' in hand and int(res['J']) == 1:
            # KKKKJ == KKKKK
            result = 6
            #print("{} is now 5 of a kind. Type {}".format(hand, result))
        else:
            result = 5
    elif 3 in res.values() and 2 in res.values():
        # Full house -- 3 of a kind and a pair
        if 'J' in hand:
            # It becomes 5 of a kind. KKKJJ (KKKKK) or JJJKK (KKKKK)
            result = 6
            #print("{} is now 5 of a kind. Type {}".format(hand, result))
        else:
            result = 4
    elif 3 in res.values():
        # Three of a kind
        if 'J' in res.keys():
            # Options: KKKJA (KKKKA) or JJJKA (KKKKA). Becomes 4 of a kind.
            result = 5
            #print("{} is now 4 of a kind. Type {}".format(hand, result))
        else:
            result = 3
    elif len([x for x in res.values() if x == 2]) == 2:
        # Two Pair
        if 'J' in res.keys():
            # Options: JJAA3 (AAAA3) or AAKKJ (AAAKK)
            if int(res['J']) == 2:
                # Becomes 4 of a kind
                result = 5
                #print("{} is now 4 of a kind. Type {}".format(hand, result))
            else:
                # Becomes Full House
                result = 4
                #print("{} is now Full House. Type {}".format(hand, result))
        else:
            result = 2
    elif len([x for x in res.values() if x == 2]) == 1:
        # One Pair
        if 'J' in res.keys():
            # JJKAQ (AAAKQ) or AAKQJ (AAAKQ). Becomes 3 of a kind
            result = 3
            #print("{} is now 3 of a kind. Type {}".format(hand, result))
        else:
            result = 2
    else:
        if 'J' in res.keys():
            result = 2
        else:
            result = 1
        #print("{} is now 1 pair. Type {}".format(hand, result))

    #print("{} is type: {}".format(hand, result))
    return result


def get_higher(a, b, part=1):
    if part == 2:
        ranking = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
    else:
        ranking = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

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


def second_order_p2(hand1, hand2):
    t1 = find_type_two(hand1)
    t2 = find_type_two(hand2)
    result = 0
    if t1 == t2:
        for x in range(5):
            if hand1[x] != hand2[x]:
                higher = get_higher(hand1[x], hand2[x], 2)
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


def rank_sort_p2(hand):
    phase_1 = sorted(hand, key=find_type_two)
    phase_2= sorted(phase_1, key=functools.cmp_to_key(second_order_p2))
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
    """Solve part 2.
    First Attempt:  250795606 -- Too High
    Second Attempt: 250769877 -- Too High
    Third Attempt:  250600944 -- Too High
    Fourth Attempt: 249541401 -- Incorrect
    """
    hand = [x[0] for x in data]
    bids = dict(data)
    ranked = rank_sort_p2(hand)
    winnings = 0
    print()
    for idx, hand in enumerate(ranked, 1):
        bid = int(bids[hand]) * idx
        print("{} has rank {} and bid: {}".format(hand, idx, bid))
        winnings += bid

    print()
    return winnings


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
