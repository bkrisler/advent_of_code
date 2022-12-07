"""AoC 2, 2022: rps."""

# Standard library imports
import pathlib
import sys
import re


def parse_data(puzzle_input):
    """Parse input."""
    pattern = re.compile('(.) (.)')
    return re.findall(pattern, puzzle_input)

def map_move(move):
    """
    Standardize the move
    """
    table = {'A': 'R', 'X': 'R', 'B': 'P', 'Y': 'P', 'C': 'S', 'Z': 'S'}
    return table[move]


def determine_win(play):
    win_table = {
        ('R', 'R'): 'T',
        ('P', 'P'): 'T',
        ('S', 'S'): 'T',
        ('R', 'S'): 'L',
        ('R', 'P'): 'W',
        ('P', 'S'): 'W',
        ('P', 'R'): 'L',
        ('S', 'P'): 'L',
        ('S', 'R'): 'W'
    }

    result = win_table[(opp := map_move(play[0]), me := map_move(play[1]))]
    return result


def score_round(move):
    choice_score = {'X': 1, 'Y': 2, 'Z': 3}
    score_map = {'W': 6, 'L': 0, 'T': 3}

    win = determine_win(move)
    score = score_map[win]
    result = choice_score[move[1]] + score
    return result


def select_required_play(move):
    """
    Given a move: (A, Y) need to play a draw so X.
    A/X = Rock, B/Y = Paper, C/Z = Sissors
    X = Loose, Y = Draw, Z = Win
    """
    strategy_table = {
        ('A', 'X'): 'Z',
        ('A', 'Y'): 'X',
        ('A', 'Z'): 'Y',
        ('B', 'X'): 'X',
        ('B', 'Y'): 'Y',
        ('B', 'Z'): 'Z',
        ('C', 'X'): 'Y',
        ('C', 'Y'): 'Z',
        ('C', 'Z'): 'X'
    }

    return strategy_table[move]


def select_and_play(move):
    selected_move = select_required_play(move)
    return score_round((move[0], selected_move))


def part1(data):
    """Solve part 1."""
    return sum([score_round(move) for move in data])


def part2(data):
    """Solve part 2."""
    return sum([select_and_play(move) for move in data])


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse_data(puzzle_input)
    yield part1(data)
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().strip())
        print("\n".join(str(solution) for solution in solutions))
