"""AoC 6, 2023: Wait For It."""

# Standard library imports
import pathlib
import re
import sys


def parse_data_one(puzzle_input):
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


def parse_data_two(puzzle_input):
    """Parse input."""
    print()
    rows = puzzle_input.split('\n')

    # What a hack!
    rows[0] = rows[0] + ' '
    rows[1] = rows[1] + ' '

    times = re.findall(r"(\d+)", rows[0])
    dists = re.findall(r"(\d+)", rows[1])
    total_time = ''
    total_dist = ''
    for x in range(len(times)):
        total_time += times[x]
        total_dist += dists[x]

    tt = int(total_time)
    td = int(total_dist)
    return tt, td


def calc_margin(time, dist):
    # Speed is 1 millimeter per 1 millisecond per millisecond button held
    # So holding the button for 1 millisecond, in a 6 millisecond race
    # results in 6 milliseconds travelled in a 7 millisecond race:
    #  hold_time * (race_time - hold_time)
    farther = []
    for hold_time in range(time+1):
        traveled = hold_time * (time - hold_time)
        if traveled > dist:
            farther.append(hold_time)

    return len(farther)


def part1(data):
    """Solve part 1."""
    result = 1
    for x in range(len(data)):
        result = result * calc_margin(data[x][0], data[x][1])

    return result


def part2(data):
    """Solve part 2."""
    result = calc_margin(data[0], data[1])
    return result


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data_one = parse_data_one(puzzle_input)
    yield part1(data_one)
    data_two = parse_data_two(puzzle_input)
    yield part2(data_two)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
        print("\n".join(str(solution) for solution in solutions))
