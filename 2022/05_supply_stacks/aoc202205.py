"""AoC 5, 2022: supply_stacks."""

# Standard library imports
import pathlib
import sys
import parse
import numpy


def parse_data(puzzle_input):
    """Parse input."""
    rows = []
    moves = []
    for line in puzzle_input.splitlines():
        if line.strip().startswith('1'):
            continue
        if line.startswith('move'):
            res = parse.parse('move {:d} from {:d} to {:d}', line)
            moves.append([res[0], res[1], res[2]])
        else:
            if len(line) > 0:
                rows.append([line[1:2], line[5:6], line[9:10]])
    result = (rows, moves)
    return result


def part1(data):
    """Solve part 1."""
    rotated_stacks = numpy.rot90(numpy.array(data[0]), 3)

    ltt = {}
    for idx in range(numpy.shape(rotated_stacks)[0]):
        ltt[idx+1] = [i for i in list(rotated_stacks[idx]) if i != ' ']

    for move in data[1]:
        for i in range(move[0]):
            move_from = ltt[move[1]]
            move_to = ltt[move[2]]
            item = move_from.pop()
            move_to.append(item)

    answer = ''
    for key in ltt:
        answer += ltt[key][-1]

    return answer


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
