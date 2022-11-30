"""AoC 2, 2018: checksum"""

# Standard library imports
import pathlib
import sys
import itertools
from collections import Counter
#from clint.textui.colored import green, blue, red


def parse(puzzle_input):
    """Parse input."""
    return puzzle_input.split()


def part1(data):
    """Solve part 1."""
    double = 0
    triple = 0

    for idd in data:
        freq = Counter(list(idd))
        double += int(2 in freq.values())
        triple += int(3 in freq.values())

    return double * triple


def build_array(m, n):
    return [[0 for _ in range(0, n)] for _ in range(0, m)]


def edit_distance(str1, str2):
    """
    The Wagner-Fischer algorithm for calculating
    edit distance between two strings.

    https://en.wikipedia.org/wiki/Wagner-Fischer_algorithm
    """
    d = build_array(len(str1) + 1, len(str2) + 1)

    s1_idx = range(len(str1))
    s2_idx = range(len(str2))

    for i in range(len(str1) + 1):
        d[i][0] = i

    for j in range(len(str2) + 1):
        d[0][j] = j

    s1_oidx = [x for x, _ in enumerate(s1_idx, 1)]
    s2_oidx = [x for x, _ in enumerate(s2_idx, 1)]

    for j in s2_oidx:
        for i in s1_oidx:
            if str1[i - 1] == str2[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min((d[i - 1][j] + 1),
                              (d[i][j - 1] + 1),
                              (d[i - 1][j - 1] + 1))

    return d[len(str1)][len(str2)], d


def calc_all_ed(codes):
    matches = []
    for a, b in itertools.combinations(codes, 2):
        e, d = edit_distance(a, b)
        if 1 == e:
            matches.append((a, b))

    return matches


def find_character_diff(str1, str2, strip=False):
    result = []
    _, m = edit_distance(str1, str2)
    for x in range(len(str1)):
        if m[x][x] == 1:
            r = ''
            for i in range(len(str1)):
                if i == x - 1:
                    if not strip:
                        r += str1[i]
                else:
                    r += str1[i]

            result.append(r)

            r = ''
            for i in range(len(str2)):
                if i == x - 1:
                    if not strip:
                        r += str2[i]
                else:
                    r += str2[i]

            result.append(r)
            return result


def part2(data):
    """Solve part 2."""
    for result in calc_all_ed(data):
       print(find_character_diff(result[0], result[1], True))


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    yield part1(data)
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().strip())
        print("\n".join(str(solution) for solution in solutions))
