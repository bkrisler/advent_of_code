"""AoC 7, 2022: no_space."""

# Standard library imports
import pathlib
import sys
from dataclasses import dataclass
from typing import Optional


@dataclass
class DirTree:
    name: str
    files: list[(int, str)]
    parent: Optional['DirTree']
    children: list['DirTree']

    def has_child(self, name):
        for child in self.children:
            if child.name == name:
                return child
        return None


def change_directory_old(cmd, crnt_dir, file_system):
    dir_name = cmd.split(' ')[-1]
    if dir_name == '..':
        # move up one directory
        crnt_dir = crnt_dir.parent
    if file_system is None:
        # First directory. Start the tree
        dir_tree = DirTree(dir_name, [], None, [])
        crnt_dir = dir_tree
    else:
        # Point to the current directory
        crnt_dir = crnt_dir.has_child(dir_name)
        if crnt_dir is None:
            # This should not ever happen
            child_dir = DirTree(dir_name, [], file_system, [])
            crnt_dir.children.append(child_dir)
            crnt_dir = child_dir

    return crnt_dir


def change_directory(cmd, crnt_dir):
    dir_name = cmd.split(' ')[-1]
    if dir_name == '/':
        while crnt_dir.parent is not None:
            crnt_dir = crnt_dir.parent
        return crnt_dir

    if dir_name == '..':
        # move up one directory
        crnt_dir = crnt_dir.parent
    else:
        # Point to the current directory
        new_dir = crnt_dir.has_child(dir_name)
        if new_dir is None:
            return crnt_dir
        else:
            crnt_dir = new_dir

    return crnt_dir


def parse_data(puzzle_input):
    """Parse input."""
    root = DirTree('/', [], None, [])
    crnt_dir = root
    commands = puzzle_input.split('$ ')
    for cmd in commands:
        scmd = cmd.strip()
        if scmd.startswith('cd'):
            crnt_dir = change_directory(scmd, crnt_dir)
        elif scmd.startswith('ls'):
            for part in scmd.splitlines():
                if part.startswith('ls'):
                    continue
                if part.startswith('dir'):
                    dname = part.split(' ')[-1]
                    tree = DirTree(dname, [], crnt_dir, [])
                    crnt_dir.children.append(tree)
                else:
                    fsize = int(part.split(' ')[0])
                    fname = part.split(' ')[1]
                    crnt_dir.files.append((fname, fsize))

    return root


def sum_dir(dt):
    total = 0
    x = {}
    for file in dt.files:
        total += file[1]

    for child in dt.children:
        child_total, x1 = sum_dir(child)
        x1[child.name] = child_total
        x = x | x1
        total += child_total

    return total, x


def calc_result(all_dirs):
    result = 0
    for key in all_dirs.keys():
        if all_dirs[key] <= 100000:
            result += all_dirs[key]

    return result


def part1(data):
    """Solve part 1."""
    dirs = {}
    top = data.name
    dirs[top], dd = sum_dir(data)
    all_dirs = dirs | dd
    result = calc_result(all_dirs)
    return result


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
