"""AoC 5, 2022: supply_stacks."""

# Standard library imports
import copy
import pathlib
import sys
from collections import defaultdict

import parse


def parse_data(puzzle_input):
    stacks = defaultdict(list)
    moves = []
    for line in puzzle_input.splitlines():
        if '[' in line:
            for i, v in enumerate(line):
                if v == '[':
                    stack_numb = int((i / 4) + 1)
                    stacks[stack_numb].insert(0, line[i+1])
        elif line.startswith('move'):
            res = parse.parse('move {:d} from {:d} to {:d}', line)
            moves.append([res[0], res[1], res[2]])

    return stacks, moves


def part1(data):
    stacks = copy.deepcopy(data[0])

    for move in data[1]:
        for i in range(move[0]):
            move_from = stacks[move[1]]
            move_to = stacks[move[2]]
            move_to.append(move_from.pop())

    answer = ''
    for x in range(len(stacks.keys())):
        answer += stacks[x+1][-1]

    return answer


def part2(data):
    """Solve part 2."""
    stacks = data[0]

    for move in data[1]:
        move_from = stacks[move[1]]
        move_to = stacks[move[2]]

        tmp = []
        start = len(move_from)
        end = start - move[0]
        for i in range(start, end, -1):
            tmp.insert(0, move_from.pop())
        move_to.extend(tmp)

    answer = ''
    for x in range(len(stacks.keys())):
        answer += stacks[x+1][-1]

    return answer


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
