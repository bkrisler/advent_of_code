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

    def pair(self):
        return self._start, self._extent

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
            x = tgt.start() - self.src.start()
            start = x + self.dest.start()

        return Range(start, tgt.extent())

    def overlapped(self, tgt):
        if tgt.start() <= self.src.start() <= tgt.end():
            start1 = self.dest.start()
            extent1 = tgt.extent() - (self.src.start() - tgt.start())

            r1 = Range(start1, extent1)
            #r2 = Range(self.src.start(), tgt.extent() - r1.extent())
            return [r1.pair()] #, r2.pair()]

        if self.src.start() <= tgt.start() <= self.src.end() <= tgt.end():
            start = self.dest.start() + (tgt.start() - self.src.start())
            r1 = Range(start, (self.dest.end() + 1) - start)
            #r2 = Range(self.src.end()+1, tgt.extent() - r1.extent())
            return [r1.pair()] #, r2.pair()]

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
            return [self.dest_range(tgt).pair()]

        # Overlap
        if self.overlaps(tgt):
            return self.overlapped(tgt)

        # # Fully outside
        # if self.outside(tgt):
        #     return [tgt.pair()]

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


def part2(data):
    """Solve part 2."""
    print("\nStart Part 2")

    seeds = list(zip(data['seeds'][::2], data['seeds'][1::2]))

    result = []
    for row in seeds:
        row_map = []
        for data_row in data['seed-to-soil']:
            r = Row(data_row)
            dst = r.dest_for_src(Range.create(row))
            if dst:
                row_map.extend(dst)
        result.extend(row_map)

    result1 = []
    for rng in result:
        row_map = []
        for data_row in data['soil-to-fertilizer']:
            r = Row(data_row)
            dst = r.dest_for_src(Range.create(rng))
            if dst:
                row_map.extend(dst)
        if not row_map:
            row_map.append(rng)
        result1.extend(row_map)

    result1 = sorted(list(dict.fromkeys(result1)), key=lambda x: x[1])
    print("Result 1: {}".format(result1))

    result2 = []
    for rng in result1:
        row_map = []
        for data_row in data['fertilizer-to-water']:
            r = Row(data_row)
            dst = r.dest_for_src(Range.create(rng))
            if dst:
                row_map.extend(dst)
        if not row_map:
            row_map.append(rng)
        result2.extend(row_map)

    result2 = sorted(list(dict.fromkeys(result2)), key=lambda x: x[1])
    print("Result 2: {}".format(result2))

    result3 = []
    for rng in result2:
        row_map = []
        for data_row in data['water-to-light']:
            r = Row(data_row)
            dst = r.dest_for_src(Range.create(rng))
            if dst:
                row_map.extend(dst)
        if not row_map:
            row_map.append(rng)
        result3.extend(row_map)

    result3 = sorted(list(dict.fromkeys(result3)), key=lambda x: x[1])
    print("Result 3: {}".format(result3))

    result4 = []
    for rng in result3:
        row_map = []
        for data_row in data['light-to-temperature']:
            r = Row(data_row)
            dst = r.dest_for_src(Range.create(rng))
            if dst:
                row_map.extend(dst)
        if not row_map:
            row_map.append(rng)
        result4.extend(row_map)

    result4 = sorted(list(dict.fromkeys(result4)), key=lambda x: x[1])
    print("Result 4: {}".format(result4))

    result5 = []
    for rng in result4:
        row_map = []
        for data_row in data['temperature-to-humidity']:
            r = Row(data_row)
            dst = r.dest_for_src(Range.create(rng))
            if dst:
                row_map.extend(dst)
        if not row_map:
            row_map.append(rng)
        result5.extend(row_map)

    result5 = sorted(list(dict.fromkeys(result5)), key=lambda x: x[1])
    print("Result 5: {}".format(result5))

    result6 = []
    for rng in result5:
        row_map = []
        for data_row in data['humidity-to-location']:
            r = Row(data_row)
            dst = r.dest_for_src(Range.create(rng))
            if dst:
                row_map.extend(dst)
        if not row_map:
            row_map.append(rng)
        result6.extend(row_map)

    result6 = sorted(list(dict.fromkeys(result6)), key=lambda x: x[1])
    print("Result: {}".format(result6))

    lowest = sorted(result6)[0][0]
    print("Lowest Location: {}".format(lowest))
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
