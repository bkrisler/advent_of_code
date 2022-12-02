"""AoC 1, 2022: calorie_counting."""

# Standard library imports
import pathlib
import sys


def parse_data(puzzle_input):
    """Parse input."""
    cals = puzzle_input.splitlines()
    elves = []
    elf = []
    for cal in cals:
        if cal == '':
            elves.append(elf)
            elf = []
        else:
            elf.append(int(cal))

    if len(elf) > 0:
        elves.append(elf)

    return elves


def part1(data):
    """Solve part 1."""
    return max(sum(entry) for entry in data)


def part2(data):
    """Solve part 2."""
    return sum(sorted([sum(entry) for entry in data], reverse=True)[0:3])


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse_data(puzzle_input)
    yield part1(data)
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().strip())
        print("\n".join(str(solution) for solution in solutions))
