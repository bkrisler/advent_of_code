"""AoC 6, 2023: Wait For It."""

# Standard library imports
import pathlib
import re
import sys


def parse_data(puzzle_input):
    """Parse input."""
    print()
    rows = puzzle_input.split('\n')

    # What a hack!
    rows[0] = rows[0] + ' '
    rows[1] = rows[1] + ' '

    times = re.findall(r"(\d+)", rows[0])
    dists = re.findall(r"(\d+)", rows[1])
    result = []
    for x in range(len(times)):
        result.append((int(times[x]), int(dists[x])))

    return result


def calc_margin(idx, x, data):
    time = data[x][0]
    dist = data[x][1]
    #options = {}
    farther = []
    for hold_time in range(time+1):
        traveled = hold_time * (time - hold_time)
        #options[hold_time] = traveled
        if traveled > dist:
            farther.append(hold_time)

    return len(farther)


def part1(data):
    """Solve part 1."""
    print()
    result = 1
    for idx, x in enumerate(range(len(data))):
        result = result * calc_margin(idx, x, data)

    return result


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
