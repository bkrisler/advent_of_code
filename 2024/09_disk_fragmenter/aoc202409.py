"""AoC 9, 2024: disk_fragmenter."""

# Standard library imports
import pathlib
import re
import sys


class DiskMap(object):
    def __init__(self, raw):
        self.raw = raw
        self.id_map = {}
        self.map = []
        self.build_map()

        for idx, f in enumerate(self.raw[::2]):
            self.id_map[idx] = f

    def build_map(self):
        freespace = self.raw[1::2]
        for idx, x in enumerate(self.raw[::2]):
            for _ in range(int(x)):
                self.map.append(str(idx))
            if idx < len(freespace):
                for _ in range(int(freespace[idx])):
                    self.map.append('.')


    def advance_end(self, dmap, idx):
        end_ptr = idx
        while dmap[end_ptr] == '.':
            end_ptr = end_ptr - 1

        return end_ptr

    def defrag(self):
        new_map = self.map.copy()
        # free_size = sum([int(x) for x in self.raw[1::2]])
        # total_size = len(self.map)

        end_ptr = len(self.map) - 1
        while new_map[end_ptr] == '.':
            end_ptr = end_ptr - 1

        for idx, v in enumerate(new_map):
            if idx >= end_ptr:
                break

            if v == '.':
                new_map[idx] = new_map[end_ptr]
                new_map[end_ptr] = '.'
                end_ptr = self.advance_end(new_map, end_ptr)

        return new_map


    def display(self):
        print('\n')
        self.defrag()
        return ''.join(self.map)


def checksum(entry):
    result = 0
    for idx, v in enumerate(entry):
        if v == '.':
            v = 0
        result += idx * int(v)
    return result

def parse_data(puzzle_input):
    """Parse input."""
    dm = DiskMap(puzzle_input)
    dm.display()
    return dm

def part1(data):
    """Solve part 1."""
    result = data.defrag()
    return checksum(result)

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
