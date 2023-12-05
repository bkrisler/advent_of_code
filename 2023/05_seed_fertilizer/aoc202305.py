"""AoC 5, 2023: Seed Fertilizer."""

# Standard library imports
import pathlib
import re
import sys

import parse


def process(row):
    parts = list(map(int, row.split(' ')))
    dest_range = [x for x in range(parts[0], parts[0] + parts[2])]
    src_range = [x for x in range(parts[1], parts[1] + parts[2])]
    row_map = zip(src_range, dest_range)
    return row_map


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
                map_data.extend(list(process(row)))
            results[title] = sorted(map_data)
            #print("{}:: {}".format(title, sorted(map_data)))

    return results


def get_match(seed, pair_map):
    seeds = [s[0] for s in pair_map]
    if seed not in seeds:
        return seed

    x = [y for y in pair_map if y[0] == seed]
    return x[0][1]



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
