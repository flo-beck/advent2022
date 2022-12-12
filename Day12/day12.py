# https://adventofcode.com/2022/day/12
from queue import Queue

from common.read_input import read_file_lines

TEST_CASE = {
    "p1_result": 31,
    "p2_result": 29,

}


class Node:
    def __init__(self, name: str, value: int, is_target: bool, x: int, y: int):
        self.name: str = name
        self.value: int = value
        self.is_target: bool = is_target
        self.x: int = x
        self.y: int = y
        self.visited: bool = False
        self.children: [Node] = []
        self.parent: Node | None = None

    def __repr__(self):
        return f'x: {self.x} y: {self.y} name: {self.name} value: {self.value}'


def get_letter_value(letter: str) -> int:
    if letter == "S":
        letter = "a"
    elif letter == "E":
        letter = "z"
    return ord(letter) - 97


def parse_grid(my_input) -> ([[Node]], Node):
    start_node: Node | None = None
    grid = []
    for y, row in enumerate(my_input):
        grid.append([])
        for x, letter in enumerate(row):
            value = get_letter_value(letter)
            target = True if letter == "E" else False
            grid[y].append(Node(letter, value, target, x, y))
            if letter == "S":
                start_node = grid[y][-1]
    return grid, start_node


def set_children_in_grid(grid: [[Node]]):
    dimensions: (int, int) = len(grid), len(grid[0])
    for y in range(0, dimensions[0]):
        for x in range(0, dimensions[1]):
            node = grid[y][x]
            # check up
            if y > 0 and grid[y - 1][x].value <= node.value + 1:
                node.children.append(grid[y - 1][x])
            # check right
            if x < (dimensions[1] - 1) and grid[y][x + 1].value <= node.value + 1:
                node.children.append(grid[y][x + 1])
            # check down
            if y < (dimensions[0] - 1) and grid[y + 1][x].value <= node.value + 1:
                node.children.append(grid[y + 1][x])
            # check left
            if x > 0 and grid[y][x - 1].value <= node.value + 1:
                node.children.append(grid[y][x - 1])


def bfs(start: Node) -> Node | None:
    my_queue = Queue()
    start.visited = True
    my_queue.put(start)
    while not my_queue.empty():
        this_node = my_queue.get()
        if this_node.is_target:
            return this_node
        for child_node in this_node.children:
            if not child_node.visited:
                child_node.visited = True
                child_node.parent = this_node
                my_queue.put(child_node)
    return None


def get_shortest_path(end: Node) -> [Node]:
    path = []
    while end.parent is not None:
        path.append(end)
        end = end.parent
    return path


def part_one(my_input):
    my_grid, start_node = parse_grid(my_input)
    set_children_in_grid(my_grid)
    end_node = bfs(start_node)
    my_path = get_shortest_path(end_node)
    return len(my_path)

# ---------------


def reset_grid(grid: [[Node]]):
    for row in grid:
        for node in row:
            node.visited = False
            node.parent = None


def find_starting_points(grid: [[Node]]) -> [Node]:
    starting_points = []
    for row in grid:
        for node in row:
            if node.value == 0:
                starting_points.append(node)
    return starting_points


def part_two(my_input):
    my_grid, start = parse_grid(my_input)
    set_children_in_grid(my_grid)
    starts = find_starting_points(my_grid)
    min_steps = 10000
    for starting_point in starts:
        reset_grid(my_grid)
        end_node = bfs(starting_point)
        if end_node is None:
            continue
        my_path = get_shortest_path(end_node)
        min_steps = min(len(my_path), min_steps)
    return min_steps


if __name__ == '__main__':
    print(f'P1 test case answer : {part_one(read_file_lines("test_input.txt"))}, expecting {TEST_CASE["p1_result"]} ')
    print(f'P1 real answer : {part_one(read_file_lines("input.txt"))} expecting 425')
    print("------------")
    print(f'P2 test case answer : {part_two(read_file_lines("test_input.txt"))}, expecting {TEST_CASE["p2_result"]} ')
    print(f'P2 real answer : {part_two(read_file_lines("input.txt"))} expecting 418')
