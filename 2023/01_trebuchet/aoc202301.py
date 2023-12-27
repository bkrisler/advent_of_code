"""AoC 1, 2023: Trebuchet."""

# Standard library imports
import pathlib
import sys
import re


def parse_data_one(puzzle_input):
    """Parse input."""
    lines = []
    for line in puzzle_input.split("\n"):
        extracted = re.findall(r'\d', line)
        lines.append(extracted)
    return lines


def parse_data_two(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split("\n")]


def part1(data):
    total = 0
    for row in data:
        r = row[0] + row[-1]
        total += int(r)
    return total


def part2(data):
    """Solve part 2."""
    total_sum = 0
    for line in data:
        line_sum = process(line)
        total_sum = total_sum + line_sum
    return total_sum


def process(line):
    txt = {'one': '1', 'two': '2', 'three': '3',
           'four': '4', 'five': '5', 'six': '6',
           'seven': '7', 'eight': '8', 'nine': '9'}

    o_line = line
    pattern = r'(?=(one|two|three|four|five|six|seven|eight|nine))'
    matches = [(m.start(), m.group(1)) for m in re.finditer(pattern, line)]
    for match in matches:
        line = line[:match[0]] + txt.get(match[1]) + line[match[0] + 1:]

    numbers = re.findall(r'\d', line)

    print("{}, {} = {}".format(o_line, line, int(numbers[0] + numbers[-1])))
    #print("{}".format(int(numbers[0] + numbers[-1])))
    return int(numbers[0] + numbers[-1])


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    #data1 = parse_data_one(puzzle_input)
    #yield part1(data1)
    data2 = parse_data_two(puzzle_input)
    yield part2(data2)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
        print("\n".join(str(solution) for solution in solutions))
