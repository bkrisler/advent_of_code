"""AoC 2, 2023: Cube Conundrum."""

# Standard library imports
import pathlib
import re
import sys
from collections import defaultdict
import json


def parse_data(puzzle_input):
    """Parse input."""
    # {game: {color: [count]}
    in_data = defaultdict(lambda: defaultdict(list))
    for row in puzzle_input.split('\n'):
        parts = row.split(":")
        game = re.match(r'Game (\d+)', parts[0]).group(1)
        sub_parts = parts[1].split(";")
        for sp in sub_parts:
            for spp in sp.split(','):
                in_data[int(game)][spp.strip().split(' ')[1]].append(int(spp.strip().split(' ')[0]))
    return in_data


def part1(data, goal):
    """Solve part 1."""
    games = list(data.keys())
    for goal_color, goal in goal.items():
        for cube_color, cube_count in data.items():
            max_count = max(cube_count[goal_color])
            if max_count > goal and cube_color in games:
                games.remove(cube_color)
    return sum(games)

        
def part2(data):
    """Solve part 2."""


def solve(puzzle_input, goal):
    """Solve the puzzle for the given input."""
    data = parse_data(puzzle_input)
    yield part1(data, goal)
    yield part2(data)


if __name__ == "__main__":
    goal = sys.argv[1]
    input_data = sys.argv[2]

    print(f"\n{input_data}:")
    #pgoal = json.load(open(pathlib.Path(goal)))
    solutions = solve(puzzle_input=pathlib.Path(input_data).read_text().rstrip(),
                      goal=json.load(open(pathlib.Path(goal))))
    print("\n".join(str(solution) for solution in solutions))
