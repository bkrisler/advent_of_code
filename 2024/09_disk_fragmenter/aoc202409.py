"""AoC 9, 2024: disk_fragmenter."""

# Standard library imports
import pathlib
import sys


class Location(object):
    def __init__(self, id_, location, size):
        self.id_ = id_
        self.location = location
        self.size = size

    def __str__(self):
        return f'Location(id={self.id_}, location={self.location}, size={self.size})'

class FreeSpace(object):
    def __init__(self, location, size):
        self.location = location
        self.size = size

    def __str__(self):
        return f'FreeSpace(location={self.location}, size={self.size})'


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


    def move(self, dmap, pos):
        added = 0
        swap_spot = -1
        for idx, x in enumerate(dmap):
            if idx < pos and x[0] == '.' and dmap[pos][1] <= x[1]:
                swap_spot = idx
                break

        if swap_spot == -1:
            return dmap, added

        # Swap the spots
        source = dmap[pos]
        target = dmap[swap_spot]
        diff = target[1] - source[1]

        # If there is remaining free space, don't loose it
        if diff > 0:
            dmap[swap_spot] = source
            dmap[pos] = ('.', source[1])
            dmap.insert(swap_spot+1, ('.', diff))
        else:
            dmap[swap_spot] = source
            dmap[pos] = target

        # Clean up free space
        result = []
        acc = 0
        for idx, v in enumerate(dmap):
            if v[0] != '.':
                if acc > 0:
                    result.append(('.', acc))
                    acc = 0
                result.append(v)
            else:
                acc += v[1]
        if acc > 0:
            result.append(('.', acc))


        return result, added

    def dump(self, row, map_):
        result = ''
        for entry in map_:
            result += ''.join([str(entry[0]) for x in range(entry[1])])
        print(f'{row}: {result}')

    def reallocate(self):
        print()
        file_id = 0
        file_map = []
        free_space = []
        pos = 0
        for idx, v in enumerate(self.raw):
            if idx % 2 == 0:
                file_map.append(Location(file_id, pos, int(v)))
                file_id += 1
            else:
                free_space.append(FreeSpace(pos, int(v)))
            pos += int(v)

        for f in sorted(file_map, key=lambda x: x.id_, reverse=True):
            #print(f'Attempt to move {f}')
            for s in sorted(free_space, key=lambda x: x.location):
                if s.location < f.location and s.size >= f.size:
                    #print(f'   {f} can move into {s}')
                    if s.size > f.size:
                        diff = s.size-f.size
                        free_space.append(FreeSpace(s.location + f.size, diff))
                    f_start = f.location
                    f.location = s.location
                    s.location = f_start
                    break

        merged = free_space + file_map
        result = []
        for loc in sorted(merged, key=lambda x: x.location):
            if isinstance(loc, FreeSpace):
                result.append('.' * loc.size)
            else:
                x = str(loc.id_) * loc.size
                result.append(x)

        #print(''.join(result))

        checksum = 0
        for x in file_map:
            for y in range(x.size):
                p = x.location + y
                checksum += p * x.id_

        return checksum


    def full_defrag(self):
        print()
        id_idx_map = []
        file_id = 0
        file_map = []
        for idx, v in enumerate(self.raw):
            if idx % 2 == 0:
                id_idx_map.append((file_id, int(v)))
                file_map.append((file_id, int(v)))
                file_id += 1
            else:
                if int(v) > 0:
                    id_idx_map.append(('.', int(v)))

        # row = 0
        # self.dump(row, id_idx_map)
        # row += 1

        new_map = id_idx_map.copy()

        for index, value in enumerate(reversed(file_map)):
            map_index = new_map.index(value)
            new_map, added = self.move(new_map, map_index)
            # self.dump(row, new_map)
            # row += 1

        return new_map


def checksum(entry):
    result = 0
    for idx, v in enumerate(entry):
        if v == '.':
            v = 0
        result += idx * int(v)
    return result


def checksum2(map_):
    result = ''
    for entry in map_:
        result += ''.join([str(entry[0]) for x in range(entry[1])])

    return checksum(result)

def parse_data(puzzle_input):
    """Parse input."""
    dm = DiskMap(puzzle_input)
    return dm

def part1(data):
    """Solve part 1."""
    result = data.defrag()
    return checksum(result)

def part2(data):
    """Solve part 2."""
    #result = data.full_defrag()
    #return checksum2(result)
    return data.reallocate()


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
