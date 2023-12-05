"""AoC 4, 2023: Scratchcards."""

# Standard library imports
import pathlib
import re
import sys
from collections import defaultdict


def parse_data(puzzle_input):
    """Parse input."""
    pattern = r'Card\s*(\d+):\s*(\d+\s*.*)\s\|\s*(\d+\s*.*)'
    cards = defaultdict(list)
    for row in puzzle_input.split('\n'):
        matches = re.finditer(pattern, row)
        for match in matches:
            winning = [x for x in match.group(2).split()]
            played = [x for x in match.group(3).split()]
            cards[match.group(1)].append(winning)
            cards[match.group(1)].append(played)

    return cards


def part1(data):
    print()
    total_points = 0
    for card, val in data.items():
        points = 0
        matches = list(set(val[0]) & set(val[1]))
        for idx, m in enumerate(matches):
            if idx == 0:
                points = 1
            else:
                points = points * 2

        total_points = total_points + points

    return total_points


def part2(data):
    """Solve part 2."""
    print()
    total_cards = 0
    card_count = defaultdict(int)
    for card, val in data.items():
        int_card = int(card)
        matches = list(set(val[0]) & set(val[1]))
        #print("Card {} has {} matching numbers".format(card, len(matches)))

        # Play my card
        for c in range(int_card + 1, int_card + len(matches) + 1):
            card_count[c] += 1

        # Play my copies
        for cc in range(card_count[int_card]):
            for c in range(int_card + 1, int_card + len(matches) + 1):
                card_count[c] += 1

    # Add all my original cards
    for card in data.keys():
        card_count[int(card)] += 1

    return sum(card_count.values())


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
