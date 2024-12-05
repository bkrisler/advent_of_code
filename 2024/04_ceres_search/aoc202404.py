"""AoC 4, 2024: ceres_search."""

# Standard library imports
import pathlib
import sys
import re


def parse_data(puzzle_input):
    """Parse input."""
    results = []
    for row in puzzle_input.split('\n'):
        results.append(list(row))

    return results

def get_val(grid, start, goal):
    row = start[0] + goal[0]
    col = start[1] + goal[1]
    if row < 0 or col < 0:
        return None, None

    try:
        result = grid[row][col]
    except IndexError:
        result = None

    return result, [(row, col), goal]

def mask_test(grid, point, mask, key):
    found = []
    for p in mask:
        v, loc = get_val(grid, point, p)
        if v == key:
            found.append(loc)
    return found

def part1(data):
    """Solve part 1."""
    # First count the rows
    pattern_fwd = 'XMAS'
    pattern_rev = 'SAMX'
    count = 0
    for r_idx, row in enumerate(data):
        matches = re.findall(pattern_fwd, ''.join(row))
        count += len(matches)
        matches = re.findall(pattern_rev, ''.join(row))
        count += len(matches)

    # Now count the columns
    rows = len(data)
    cols = len(data[0])
    columns = []
    for c_idx in range(0, cols):
        column = []
        for r_idx in range(0, rows):
            column.append(data[r_idx][c_idx])

        matches = re.findall(pattern_fwd, ''.join(column))
        count += len(matches)
        matches = re.findall(pattern_rev, ''.join(column))
        count += len(matches)
        columns.append(column)

    # Now for the diags
    mask = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
    for r_idx, row in enumerate(data):
        for c_idx, value in enumerate(row):
            if value == 'X':
                found_m = mask_test(data, (r_idx, c_idx), mask, 'M')
                for mp in found_m:
                    found_a = mask_test(data, mp[0], [mp[1]], 'A')
                    for fa in found_a:
                        found_s = mask_test(data, fa[0], [fa[1]], 'S')
                        count += len(found_s)

    return count


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
