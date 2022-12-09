# https://adventofcode.com/2022/day/7
from enum import Enum

from common.read_input import read_file_lines

TEST_CASE = {
    "p1_result": 95437,
    "p2_result": 24933642,

}


class FileType(Enum):
    DIR = 0
    FILE = 1


class Node:
    def __init__(self, parent, filetype: FileType, name: str, size: int):
        self.parent: Node = parent
        self.type: FileType = filetype
        self.children: [Node] = []
        self.name: str = name
        self.size: int = size

    def __repr__(self):
        match self.type:
            case FileType.DIR:
                return f'{self.name} (dir, size={self.size})'
            case FileType.FILE:
                return f'{self.name} (file, size={self.size})'


def print_filesystem(node: Node, num_spaces: int):
    spaces = ' ' * num_spaces
    print(f'{spaces}- {node}')
    for node in node.children:
        print_filesystem(node, num_spaces + 2)


def do_cd(cd_arg: str, current: Node, start: Node) -> Node:
    match cd_arg:
        case "..":
            return current.parent
        case "/":
            return start
        case _:
            for node in current.children:
                if node.name == cd_arg:
                    return node
            raise ValueError(f'Cannot cd {cd_arg} - not found on current node')


def calc_sizes(current_node: Node) -> int:
    if current_node.type == FileType.DIR:
        for node in current_node.children:
            current_node.size += calc_sizes(node)
    return current_node.size


def find_total_size_of_dirs_under_size(current_node: Node, total: int):
    if current_node.type == FileType.DIR:
        for node in current_node.children:
            total = find_total_size_of_dirs_under_size(node, total)
        if current_node.size <= 100000:
            total += current_node.size
    return total


def create_filesystem_tree(my_input) -> Node:
    start: Node = Node(None, FileType.DIR, "/", 0)
    current: Node = start
    for line in my_input:
        if line[0] == '$':  # we have a command
            split = line.split(" ")
            if split[1] == "cd":
                current = do_cd(split[2], current, start)
        else:
            split = line.split(" ")
            if split[0] == "dir":
                current.children.append(Node(current, FileType.DIR, split[1], 0))
            else:
                current.children.append(Node(current, FileType.FILE, split[1], int(split[0])))
    return start


def part_one(my_input):
    filesystem = create_filesystem_tree(my_input)
    calc_sizes(filesystem)
    # print_filesystem(filesystem, 0)
    return find_total_size_of_dirs_under_size(filesystem, 0)


# ---------------


def find_smallest_dir_of_size(current_node: Node, space_size: int, smallest_dir: Node | None) -> Node:
    if current_node.type == FileType.DIR:
        for node in current_node.children:
            smallest_dir = find_smallest_dir_of_size(node, space_size, smallest_dir)
        if current_node.size >= space_size and (smallest_dir is None or current_node.size < smallest_dir.size):
            smallest_dir = current_node
    return smallest_dir


def part_two(my_input):
    filesystem = create_filesystem_tree(my_input)
    calc_sizes(filesystem)
    unused_disk_space = 70000000 - filesystem.size
    disk_space_to_free = 30000000 - unused_disk_space
    return find_smallest_dir_of_size(filesystem, disk_space_to_free, None).size


if __name__ == '__main__':
    print(f'P1 test case answer : {part_one(read_file_lines("test_input.txt"))}, expecting {TEST_CASE["p1_result"]} ')
    print(f'P1 real answer : {part_one(read_file_lines("input.txt"))} expecting 1915606')
    print("------------")
    print(f'P2 test case answer : {part_two(read_file_lines("test_input.txt"))}, expecting {TEST_CASE["p2_result"]} ')
    print(f'P2 real answer : {part_two(read_file_lines("input.txt"))} expecting 5025657 (NOT rlbhdgm)')
