"""AoC 8, 2023: Haunted Wasteland."""

# Standard library imports
import pathlib
import re
import sys
from collections import defaultdict
from math import lcm


def parse_data(puzzle_input):
    """Parse input."""
    nodes = {}
    for idx, row in enumerate(puzzle_input.split('\n')):
        if idx == 0:
            nodes['navigate'] = row
        elif idx == 1:
            continue
        else:
            res = re.findall(r"(\w+) = .(\w+), (\w+).", row)
            nodes[res[0][0]] = {'L': res[0][1], 'R': res[0][2]}

    return nodes


def part1(data):
    """Solve part 1."""
    print()
    nav = [*data['navigate']]
    nxt_node = 'AAA'
    sz = len(nav)
    steps = idx = 0
    while idx <= sz:
        nxt_node = data[nxt_node][nav[idx]]
        steps += 1
        idx += 1
        if nxt_node == 'ZZZ':
            break
        if idx == sz:
            idx = 0

    return steps


def part2_orig(data):
    """Solve part 2.
    Attempt One: 913793 is too low
    """
    print()
    nav = [*data['navigate']]
    next_nodes = [x for x in data.keys() if x[-1] == 'A']
    sz = len(nav)
    steps = idx = 0
    loops = defaultdict(list)
    check = None
    sep = 0
    turns = []
    while idx <= sz:
        next_nodes = [data[entry][nav[idx]] for entry in next_nodes]
        turns.append(nav[idx])
        if check is None:
            check = next_nodes[0]
        for ix, n in enumerate(next_nodes):
            if n == check and n in loops[ix]:
                print("{}/{} - {}: {}".format(check, loops[ix][-1], "".join(turns), sep))
                sep = 0
                turns = []
            else:
                sep += 1
            loops[ix].append(n)
        steps += 1
        idx += 1
        end = [entry[-1] for entry in next_nodes]
        end_same = all(c == end[0] for c in end)
        #print("Step: {}, End: {}".format(steps, end))
        if end_same and end[0] == 'Z':
            break
        if idx == sz:
            #print(loops)
            idx = 0

    return steps


def part2(data):
    """Solve part 2.
    Attempt One: 913793 is too low
    """
    print()
    nav = [*data['navigate']]
    next_nodes = [x for x in data.keys() if x[-1] == 'A']
    node_a = next_nodes[0]
    sz = len(nav)
    steps = idx = 0
    paths = {}
    while idx <= sz:
        next_nodes = [data[entry][nav[idx]] for entry in next_nodes]
        steps += 1
        idx += 1
        #print("Step: {}, End: {}".format(steps, end))
        for x, n in enumerate(next_nodes):
            if n[-1] == 'Z':
                paths[x] = steps
                if len(paths.keys()) == len(next_nodes):
                    vv = list(paths.values())
                    result = lcm(*vv)
                    return result
        if idx == sz:
            #print(loops)
            idx = 0

    return steps

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
