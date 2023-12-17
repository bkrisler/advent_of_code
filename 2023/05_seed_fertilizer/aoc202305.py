"""AoC 5, 2023: Seed Fertilizer."""

# Standard library imports
import pathlib
import re
import sys
from collections import defaultdict


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
            return Range(start1, extent1).pair()

        if self.src.start() <= tgt.start() <= self.src.end() <= tgt.end():
            start = self.dest.start() + (tgt.start() - self.src.start())
            extent = (self.dest.end() + 1) - start
            remainder = tgt.start() + extent, tgt.end() + 1 - (tgt.start() + extent)
            return Range(start, extent).pair(), remainder

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
            return self.dest_range(tgt).pair()

        # Overlap
        if self.overlaps(tgt):
            return self.overlapped(tgt)

    def unmapped(self, src):
        if self.overlaps(src):
            ovr = self.overlaps(src)
            print("Overlapped: {}, Source: {}".format(ovr, src))
        elif self.outside(src):
            return src

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


def get_mapped(row, seed):
    r = Row(row)
    s = Range.create(seed)
    mapped = r.dest_for_src(s)
    unmapped = r.unmapped(s)
    return mapped, unmapped


def row_match(inn, data):
    in_range = Range.create(inn)
    result = defaultdict(list)
    for row in data:
        r = Row(row)
        if r.src_contains(in_range) or r.overlaps(in_range):
            result[inn].append(row)

    return result


def advance_row(inn, data, map_name):
    print("\n{} with: {}".format(map_name, sorted(inn)))
    nxt_row = []
    matched = None
    for seed in inn:
        matched = row_match(seed, data)
        for k, v in matched.items():
            for vv in v:
                if Row(vv).src_contains(Range.create(k)):
                    nxt_row.append([Row(vv).dest_for_src(Range.create(k))])
                else:
                    print("Partial")

    if not matched:
        return inn

    return [y[0] for y in nxt_row]


def process_overlap(seed, data):
    result = []
    for d in data:
        print("Here: {} and {}".format(seed, d))
        x, remainder = Row(d).overlapped(Range.create(seed))
        result.append(x)

        if x[1] < Range.create(seed).extent():
            print("We have extra to deal with")

    return result


def process_seed(seed, data):
    result = defaultdict(lambda: defaultdict(list))
    s = Range.create(seed)
    for row in data:
        if Row(row).src_contains(s):
            result[seed]['contains'].append(row)
        elif Row(row).overlaps(s):
            result[seed]['overlaps'].append(row)
        else:
            result[seed]['outside'].append(row)

    if result[seed]['contains']:
        answer = Row(result[seed]['contains'][0]).dest_for_src(s)
        return answer

    if result[seed]['overlaps']:
        return process_overlap(seed, result[seed]['overlaps'])

    return seed


def poverlap(seed, data):
    result = []
    for d in data:
        print("Here: {} and {}".format(seed, d))
        x, remainder = Row(d).overlapped(Range.create(seed))
        result.append(x)
        if remainder:
            result.append(poverlap(seed, data))

    return result


def pseed(seed, data):
    s = Range.create(seed)
    for row in data:
        r = Row(row)
        if r.src_contains(s):
            return r.dest_for_src(s)
        elif r.overlaps(s):
            result = poverlap(s)
            print(result)

    return None


def src_end(row):
    return row[1] + (row[2] - 1)


def dest_start(seed, row):
    return row[0] + (seed[0] - row[1])


def next_seed(seed, row, nxt_row):
    if seed[0] >= row[1] and seed[0] + (seed[1] - 1) <= row[1] + (row[2] - 1):
        # Fully contains
        ds = dest_start(seed, row)
        return [(ds, seed[1])]
    elif seed[0] >= row[1] and seed[0] + (seed[1] - 1) > row[1] + (row[2] - 1):
        # Overlaps
        if nxt_row is not None:
            if row[1] + (row[2] - 1) != nxt_row[1] - 1:
                #print("There is a gap! Row A ends at: {} and Row B starts at: {}".format(row[1] + (row[2] - 1), nxt_row[1]))
                p3x = row[1] + (row[2])
                p3y = nxt_row[1] - 1
                p3 = (p3x, p3y)
                p1_start = dest_start(seed, row)
                p1_extent = (row[0] + row[2]) - p1_start
                p1 = (p1_start, p1_extent)
                nxt_seed = seed[0] + p1_extent, seed[1] - p1_extent
                p2a = dest_start(nxt_seed, nxt_row)
                p2 = (p2a, nxt_seed[1])
                return [p1, p2, p3]
            else:
                p1_start = dest_start(seed, row)
                p1_extent = (row[0] + row[2]) - p1_start
                p1 = (p1_start, p1_extent)
                nxt_seed = seed[0] + p1_extent, seed[1] - p1_extent
                p2a = dest_start(nxt_seed, nxt_row)
                p2 = (p2a, nxt_seed[1])
                return [p1, p2]
        else:
            ds = dest_start(seed, row)
            if seed[1] > row[2] - (seed[0] - row[1]):
                p1 = ds, (seed[0] - row[1])
                p2 = seed[0] + (seed[0] - row[1]), seed[1] - (seed[0] - row[1])
                return [p1, p2]


def get_next(seed, data):
    sorted_data = sorted(data, key=lambda x: x[1])
    for idx, row in enumerate(sorted_data):
        if row[1] <= seed[0] <= src_end(row):
            nr = sorted_data[idx+1] if len(sorted_data) > idx+1 else None
            return next_seed(seed, row, nr)

    return [seed]


def part2(data):
    seeds = list(zip(data['seeds'][::2], data['seeds'][1::2]))

    result = []
    print("Seed-to-soil")
    for seed in sorted(seeds):
        nxt = get_next(seed, data['seed-to-soil'])
        result.extend(nxt)
        print("{} converts to {}".format(seed, nxt))

    result2 = []
    print("\nSoil-to-fertilizer")
    for seed in sorted(result):
        nxt = get_next(seed, data['soil-to-fertilizer'])
        result2.extend(nxt)
        print("{} converts to {}".format(seed, nxt))

    result3 = []
    print("\nFertilizer-to-water")
    for seed in sorted(result2):
        nxt = get_next(seed, data['fertilizer-to-water'])
        result3.extend(nxt)
        print("{} converts to {}".format(seed, nxt))

    result4 = []
    print("\nWater-to-light")
    for seed in sorted(result3):
        nxt = get_next(seed, data['water-to-light'])
        result4.extend(nxt)
        print("{} converts to {}".format(seed, nxt))

    result5 = []
    print("\nLight-to-temperature")
    for seed in sorted(result4):
        nxt = get_next(seed, data['light-to-temperature'])
        result5.extend(nxt)
        print("{} converts to {}".format(seed, nxt))

    result6 = []
    print("\nTemperature-to-humidity")
    for seed in sorted(result5):
        nxt = get_next(seed, data['temperature-to-humidity'])
        result6.extend(nxt)
        print("{} converts to {}".format(seed, nxt))

    result7 = []
    print("\nHumidity-to-location")
    for seed in sorted(result6):
        nxt = get_next(seed, data['humidity-to-location'])
        result7.extend(nxt)
        print("{} converts to {}".format(seed, nxt))

    print()

    return sorted(result6)[0][0]


def part2_2(data):
    inn = list(zip(data['seeds'][::2], data['seeds'][1::2]))

    a = advance_row(inn, data['seed-to-soil'], 'seed-to-soil')
    b = advance_row(a, data['soil-to-fertilizer'], 'soil-to-fertilizer')
    c = advance_row(b, data['fertilizer-to-water'], 'fertilizer-to-water')

    print("Result for Fertilizer-to-Waster: {}".format(sorted(c)))


def part2_orig(data):
    """Solve part 2."""
    print("\nStart Part 2")

    input = list(zip(data['seeds'][::2], data['seeds'][1::2]))
    result = []
    print("Seed to Soil")
    for row in data['seed-to-soil']:
        for seed in input:
            mapped, unmapped = get_mapped(row, seed)
            if mapped:
                result.append(mapped)
                print("Seed: {} maps to: {}".format(seed, mapped))
            if unmapped:
                print("Seed: {} also maps to: {}".format(seed, unmapped))


    input = result.copy()
    print("Soil To Fertilizer")
    for row in data['soil-to-fertilizer']:
        for seed in input:
            mapped, unmapped = get_mapped(row, seed)
            if mapped:
                print("Seed: {} maps to: {}".format(seed, mapped))
            if unmapped:
                print("Seed: {} also maps to: {}".format(seed, unmapped))


    # result = []
    # for row in seeds:
    #     row_map = []
    #     for data_row in data['seed-to-soil']:
    #         r = Row(data_row)
    #         dst = r.dest_for_src(Range.create(row))
    #         if dst:
    #             row_map.extend(dst)
    #     result.extend(row_map)
    #
    # result1 = []
    # for rng in result:
    #     row_map = []
    #     for data_row in data['soil-to-fertilizer']:
    #         r = Row(data_row)
    #         dst = r.dest_for_src(Range.create(rng))
    #         if dst:
    #             row_map.extend(dst)
    #     if not row_map:
    #         row_map.append(rng)
    #     result1.extend(row_map)
    #
    # result1 = sorted(list(dict.fromkeys(result1)), key=lambda x: x[1])
    # print("Result 1: {}".format(result1))
    #
    # result2 = []
    # for rng in result1:
    #     row_map = []
    #     for data_row in data['fertilizer-to-water']:
    #         r = Row(data_row)
    #         dst = r.dest_for_src(Range.create(rng))
    #         if dst:
    #             row_map.extend(dst)
    #     if not row_map:
    #         row_map.append(rng)
    #     result2.extend(row_map)
    #
    # result2 = sorted(list(dict.fromkeys(result2)), key=lambda x: x[1])
    # print("Result 2: {}".format(result2))
    #
    # result3 = []
    # for rng in result2:
    #     row_map = []
    #     for data_row in data['water-to-light']:
    #         r = Row(data_row)
    #         dst = r.dest_for_src(Range.create(rng))
    #         if dst:
    #             row_map.extend(dst)
    #     if not row_map:
    #         row_map.append(rng)
    #     result3.extend(row_map)
    #
    # result3 = sorted(list(dict.fromkeys(result3)), key=lambda x: x[1])
    # print("Result 3: {}".format(result3))
    #
    # result4 = []
    # for rng in result3:
    #     row_map = []
    #     for data_row in data['light-to-temperature']:
    #         r = Row(data_row)
    #         dst = r.dest_for_src(Range.create(rng))
    #         if dst:
    #             row_map.extend(dst)
    #     if not row_map:
    #         row_map.append(rng)
    #     result4.extend(row_map)
    #
    # result4 = sorted(list(dict.fromkeys(result4)), key=lambda x: x[1])
    # print("Result 4: {}".format(result4))
    #
    # result5 = []
    # for rng in result4:
    #     row_map = []
    #     for data_row in data['temperature-to-humidity']:
    #         r = Row(data_row)
    #         dst = r.dest_for_src(Range.create(rng))
    #         if dst:
    #             row_map.extend(dst)
    #     if not row_map:
    #         row_map.append(rng)
    #     result5.extend(row_map)
    #
    # result5 = sorted(list(dict.fromkeys(result5)), key=lambda x: x[1])
    # print("Result 5: {}".format(result5))
    #
    # result6 = []
    # for rng in result5:
    #     row_map = []
    #     for data_row in data['humidity-to-location']:
    #         r = Row(data_row)
    #         dst = r.dest_for_src(Range.create(rng))
    #         if dst:
    #             row_map.extend(dst)
    #     if not row_map:
    #         row_map.append(rng)
    #     result6.extend(row_map)
    #
    # result6 = sorted(list(dict.fromkeys(result6)), key=lambda x: x[1])
    # print("Result: {}".format(result6))
    #
    # lowest = sorted(result6)[0][0]
    # print("Lowest Location: {}".format(lowest))
    # return lowest


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
