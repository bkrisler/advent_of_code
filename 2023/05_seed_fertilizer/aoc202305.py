"""AoC 5, 2023: Seed Fertilizer."""
import concurrent.futures

# Standard library imports
import pathlib
import re
import sys


def parse_data(puzzle_input):
    """Parse input."""

    results = {}
    matches = re.finditer(r'([a-z].+):((\s+\d+)*)', puzzle_input)
    for match in matches:
        title = match.group(1).strip()
        if title == 'seeds':
            seeds = match.group(2).strip().split(' ')
            #print("process seeds: {}".format(seeds))
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
            #print("{}:: {}".format(title, sorted(map_data)))

    return results


def get_match(seed, pair_map):
    l = [x for x in sorted(pair_map, key = lambda x: x[1]) if x[1] <= seed]
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

        #print("Seed: {}, Soil: {}, Fertilizer: {}, Water: {}, Light: {}, Temp: {}, Humidity: {} Location: {}".format(seed, soil, fertilizer, water, light, temp, humidity, location))
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

    #print("Seed: {}, Soil: {}, Fertilizer: {}, Water: {}, Light: {}, Temp: {}, Humidity: {} Location: {}".format(seed, soil, fertilizer, water, light, temp, humidity, location))
    return location


def process_entry(entry, data):
    min_location = sys.maxsize

    for seed in range(entry[0], entry[0] + entry[1]):
        location = get_location(seed, data)
        if location < min_location:
            min_location = location
            #print("Min = {}".format(min_location))
    return min_location


def part2(data):
    """Solve part 2."""
    print("\nStart Part 2")

    min_location = sys.maxsize
    pairs = zip(data['seeds'][::2], data['seeds'][1::2])

    for entry in pairs:
        m = process_entry(entry, data)
        if m < min_location:
            min_location = m

    # executor = concurrent.futures.ProcessPoolExecutor(10)
    # futures = [executor.submit(process_entry, entry, data) for entry in pairs]
    # concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)

    # merged_list = [v for f in futures for v in f.result()]
    # print(merged_list)
    # min_location = min(merged_list)

#        print("Processing: {} with {} seeds".format(entry, entry[1]))

    return min_location


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
