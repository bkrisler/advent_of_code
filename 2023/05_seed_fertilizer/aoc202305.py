"""AoC 5, 2023: Seed Fertilizer."""

# Standard library imports
import pathlib
import re
import sys


class Range:
    def __init__(self, start=0, extent=0):
        self._start = start
        self._extent = extent

    @staticmethod
    def create(pnt):
        return Range(pnt[0], pnt[1])

    def start(self):
        return self._start

    def end(self):
        if self._extent == 0:
            # This makes no sense, but try to cover it?
            return self._start

        return self._start + (self._extent - 1)

    def extent(self):
        return self._extent

    def contains(self, r):
        return r.start() >= self._start and r.end() <= self.end()

    def __eq__(self, other):
        return self._start == other.start() and self._extent == other.extent()

    def __str__(self):
        return "Range: {}, {}".format(self._start, self._extent)

    def __repr__(self):
        return "{}, {}".format(self._start, self._extent)

    @staticmethod
    def from_row(data):
        src = Range(data[1], data[2])
        dest = Range(data[0], data[2])
        return src, dest


class Row:
    def __init__(self, row):
        self._row = row
        self.src = Range(self._row[1], self._row[2])
        self.dest = Range(self._row[0], self._row[2])

    def get_src(self):
        return self.src

    def get_dest(self):
        return self.dest

    def src_contains(self, r):
        return self.src.contains(r)

    def dest_range(self, tgt):
        if tgt.start() == self.src.start():
            start = self.dest.start()
        else:
            start = self.src.start() + ((tgt.start() - 1) - self.src.end())

        return Range(start, tgt.extent())

    def overlapped(self, tgt):
        if tgt.start() <= self.src.start() <= tgt.end():
            if tgt.start() == self.src.start():
                start1 = self.dest.start()
                extent1 = self.dest.extent()
            else:
                start1 = self.src.start() - (self.src.start() - tgt.start())
                extent1 = self.src.start() - start1

            r1 = Range(start1, extent1)
            r2 = Range(self.src.start(), tgt.extent() - r1.extent())
            return [r1, r2]

        if self.src.start() <= tgt.start() <= self.src.end() <= tgt.end():
            start = self.src.start() + ((tgt.start() - 1) - self.src.end())
            r1 = Range(start, (self.dest.end() + 1) - start)
            r2 = Range(self.src.end()+1, tgt.extent() - r1.extent())
            return [r1, r2]

    def overlaps(self, tgt):
        if tgt.start() <= self.src.start() <= tgt.end():
            return True

        if self.src.start() <= tgt.start() <= self.src.end() <= tgt.end():
            return True

        return False

    def outside(self, tgt):
        if tgt.end() < self.src.start():
            return True

        if tgt.start() > self.src.end():
            return True

        return False

    def dest_for_src(self, tgt):
        # Fully contained
        if self.src_contains(tgt):
            return [self.dest_range(tgt)]

        # Overlap
        if self.overlaps(tgt):
            return self.overlapped(tgt)

        # Fully outside
        if self.outside(tgt):
            return [tgt]

    def __repr__(self):
        return "Row: Src: {}, Dest: {}".format(self.src, self.dest)


def parse_data(puzzle_input):
    """Parse input."""

    results = {}
    matches = re.finditer(r'([a-z].+):((\s+\d+)*)', puzzle_input)
    for match in matches:
        title = match.group(1).strip()
        if title == 'seeds':
            seeds = match.group(2).strip().split(' ')
            # print("process seeds: {}".format(seeds))
            seeds = list(map(int, seeds))
            results[title] = seeds
        else:
            if title.endswith('map'):
                title = title.strip(' map')
            m = match.group(2).strip()

            map_data = []
            for row in m.splitlines():
                map_data.append(list(map(int, row.split(' '))))
            results[title] = sorted(map_data)

            # print("{}:: {}".format(title, sorted(map_data)))

    return results


def get_match(seed, pair_map):
    l = [x for x in sorted(pair_map, key=lambda x: x[1]) if x[1] <= seed]
    if not l:
        return seed

    closest = l[-1]
    r_min = closest[1]
    r_max = closest[1] + closest[2]
    if r_min <= seed <= r_max:
        index = seed - r_min
        return closest[0] + index

    return seed


def part1(data):
    """Solve part 1."""
    print()

    locations = []

    for seed in data['seeds']:
        # Get Soil Number
        soil = get_match(seed, data['seed-to-soil'])

        # Get fertilizer Number
        fertilizer = get_match(soil, data['soil-to-fertilizer'])

        # Get Water Number
        water = get_match(fertilizer, data['fertilizer-to-water'])

        # Get Light Number
        light = get_match(water, data['water-to-light'])

        # Get Temperature Number
        temp = get_match(light, data['light-to-temperature'])

        # Get Humidity Number
        humidity = get_match(temp, data['temperature-to-humidity'])

        # Get Location Number
        location = get_match(humidity, data['humidity-to-location'])

        # print("Seed: {}, Soil: {}, Fertilizer: {}, Water: {}, Light: {}, Temp: {}, Humidity: {} Location: {}".format(seed, soil, fertilizer, water, light, temp, humidity, location))
        locations.append(location)

    return min(locations)


def get_location(seed, data):
    # print("  Seed: {}".format(seed))
    # Get Soil Number
    soil = get_match(seed, data['seed-to-soil'])

    # Get fertilizer Number
    fertilizer = get_match(soil, data['soil-to-fertilizer'])

    # Get Water Number
    water = get_match(fertilizer, data['fertilizer-to-water'])

    # Get Light Number
    light = get_match(water, data['water-to-light'])

    # Get Temperature Number
    temp = get_match(light, data['light-to-temperature'])

    # Get Humidity Number
    humidity = get_match(temp, data['temperature-to-humidity'])

    # Get Location Number
    location = get_match(humidity, data['humidity-to-location'])

    print("Seed: {}, Soil: {}, Fertilizer: {}, Water: {}, Light: {}, Temp: {}, Humidity: {} Location: {}".format(seed,
                                                                                                                 location))
    return location


def range_end(r):
    return r[0] + (r[1] - 1)


def src_range(container):
    return container[1], container[2]


def dest_range(container):
    return container[0], container[2]


def contains(container, target):
    return target[0] >= src[0] and range_end(target) <= range_end((container[1], container[2]))


def outside(container, target):
    # print("{} > {} or {} < {}".format(
    #     target[0], container[1]+(container[2]-1), target[0] + target[1], container[1]))
    if target[0] > container[1] + (container[2] - 1) or target[0] + target[1] < container[1]:
        return True


def overlap(container, target):
    if target[0] < container[1] <= range_end(target):
        return True

    if container[1] < target[0] < range_end((container[1], container[2])):
        return True

    return False


def get_destination(target, data):
    start_index = data[0] + (target[0] - data[1])
    return start_index, target[1]


def get_overlap_dest(target, data):
    if target[0] - data[1] < 0:
        a_start = target[0]
        a_end = data[1] - 1
        b_start = data[0]
        b_end = target[1] - (a_end - (a_start - 1))

        r1 = a_start, a_end - (a_start - 1)
        r2 = b_start, b_end,

    else:
        dest_start = data[0] + (target[0] - data[1])
        src_end = data[1] + (data[2] - 1)
        dest_end = data[0] + (data[2] - 1)

        r1 = dest_start, (dest_end + 1 - dest_start)
        r2 = src_end + 1, (target[1] - r1[1])

    return [r1, r2]


def map_range(tgt, data):
    tr = Range.create(tgt)
    row = Row(data)

    if row.src_contains(tr):
        return [row.dest_range(tr)]

    # match = [row for row in sorted(data) if contains(row, tgt)]
    # if match:
    #     return [get_destination(tgt, match[0])]

    overlap_match = [row for row in sorted(data, key=lambda x: x[1]) if overlap(row, tgt)]
    if overlap_match:
        overlaps = []
        for o in overlap_match:
            overlaps.append(get_overlap_dest(tgt, o))
        lll = [item for sub_list in overlaps for item in sub_list]
        return lll

    outside_match = [row for row in sorted(data) if outside(row, tgt)]
    if len(outside_match) == len(data):
        return [tgt]

    raise Exception("Why?")


def part2(data):
    """Solve part 2."""
    print("\nStart Part 2")

    seeds = list(zip(data['seeds'][::2], data['seeds'][1::2]))

    result = []
    for row in seeds:
        for x in map_range(row, data['seed-to-soil']):
            result.append(x)

    result2 = []
    for row in result:
        for x in map_range(row, data['soil-to-fertilizer']):
            result2.append(x)

    result3 = []
    for row in result2:
        for x in map_range(row, data['fertilizer-to-water']):
            result3.append(x)

    result4 = []
    for row in result3:
        for x in map_range(row, data['water-to-light']):
            result4.append(x)

    result5 = []
    for row in result4:
        for x in map_range(row, data['light-to-temperature']):
            result5.append(x)

    result6 = []
    for row in result5:
        for x in map_range(row, data['temperature-to-humidity']):
            result6.append(x)

    result7 = []
    for row in result6:
        for x in map_range(row, data['humidity-to-location']):
            result7.append(x)

    lowest = sorted(result7)[0][0]
    # print("Lowest Location: {}".format(lowest))
    return lowest


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
