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
