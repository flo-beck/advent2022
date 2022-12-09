# https://adventofcode.com/2022/day/8
from enum import Enum

from common.read_input import read_file_lines

TEST_CASE = {
    "p1_result": 21,
    "p2_result": 8,

}


class Tree:
    def __init__(self, x: int, y: int, size: int):
        self.x: int = x
        self.y: int = y
        self.size: int = size
        self.visible: bool = False
        self.scenic_score = 0

    def calc_scenic_score(self, new_value: int):
        self.scenic_score = self.scenic_score * new_value if self.scenic_score > 0 else new_value

    def __repr__(self):
        if self.visible:
            return f'[{self.size}]'
        else:
            return f' {self.size} '


def create_forest(my_input):
    forest = []
    for y, line in enumerate(my_input):
        forest.append([])
        for x, tree in enumerate(line):
            forest[y].append(Tree(x, y, int(line[x])))
    return forest


def print_forest(forest: [[Tree]]):
    for row in forest:
        for tree in row:
            print(tree, end='')
        print('')


def if_tree_on_edge(tree: Tree, forest: [[Tree]]):
    x_max = len(forest[0]) - 1
    y_max = len(forest) - 1
    if tree.x == 0 or tree.x == x_max or tree.y == 0 or tree.y == y_max:
        return True
    return False


def get_tree_range_from_edge(end: Tree, x_dir: int, y_dir: int, forest: [[Tree]]) -> [Tree]:
    tree_range = []
    if y_dir != 0:
        y_start = 0 if y_dir > 0 else len(forest) - 1
        for y in range(y_start, end.y, y_dir):
            tree_range.append(forest[y][end.x])
    else:
        x_start = 0 if x_dir > 0 else len(forest[0]) - 1
        for x in range(x_start, end.x, x_dir):
            tree_range.append(forest[end.y][x])
    return tree_range


def is_visible_from_dir(tree: Tree, x_dir: int, y_dir: int, forest: [[Tree]]):
    tree_range = get_tree_range_from_edge(tree, x_dir, y_dir, forest)
    for this_tree in tree_range:
        if this_tree.size >= tree.size:
            return False
    return True


def set_visible(forest: [[Tree]]):
    for row in forest:
        for tree in row:
            if if_tree_on_edge(tree, forest):
                tree.visible = True
            else:
                if is_visible_from_dir(tree, 0, 1, forest) or is_visible_from_dir(tree, 1, 0, forest) \
                        or is_visible_from_dir(tree, 0, -1, forest) or is_visible_from_dir(tree, -1, 0, forest):
                    tree.visible = True


def count_visible_trees(forest: [[Tree]]) -> int:
    count = 0
    for row in forest:
        for tree in row:
            if tree.visible:
                count += 1
    return count


def part_one(my_input):
    forest = create_forest(my_input)
    set_visible(forest)
    # print_forest(forest)
    return count_visible_trees(forest)


# ---------------

def calc_visible_trees(tree_range: [Tree], my_tree: Tree) -> int:
    visible_trees = 0
    for tree in tree_range:
        visible_trees += 1
        if tree.size >= my_tree.size:
            break
    return visible_trees


def get_tree_range_to_edge(start: Tree, x_dir: int, y_dir: int, forest: [[Tree]]) -> [Tree]:
    tree_range = []
    if y_dir != 0:
        y_max = -1 if y_dir < 0 else len(forest)
        for y in range(start.y + y_dir, y_max, y_dir):
            tree_range.append(forest[y][start.x])
    else:
        x_max = -1 if x_dir < 0 else len(forest[0])
        for x in range(start.x + x_dir, x_max, x_dir):
            tree_range.append(forest[start.y][x])
    return tree_range


def calc_scenic_scores(forest: [[Tree]]):
    for y in range(1, len(forest) - 1):
        for x in range(1, len(forest[0]) - 1):
            my_tree = forest[y][x]
            forest[y][x].calc_scenic_score(calc_visible_trees(get_tree_range_to_edge(my_tree, 0, -1, forest), my_tree))
            forest[y][x].calc_scenic_score(calc_visible_trees(get_tree_range_to_edge(my_tree, -1, 0, forest), my_tree))
            forest[y][x].calc_scenic_score(calc_visible_trees(get_tree_range_to_edge(my_tree, 0, 1, forest), my_tree))
            forest[y][x].calc_scenic_score(calc_visible_trees(get_tree_range_to_edge(my_tree, 1, 0, forest), my_tree))


def find_highest_scenic_score(forest: [[Tree]]) -> int:
    result = 0
    for row in forest:
        for tree in row:
            if tree.scenic_score > result:
                result = tree.scenic_score
    return result


def part_two(my_input):
    forest = create_forest(my_input)
    # print_forest(forest)
    calc_scenic_scores(forest)
    return find_highest_scenic_score(forest)


if __name__ == '__main__':
    print(f'P1 test case answer : {part_one(read_file_lines("test_input.txt"))}, expecting {TEST_CASE["p1_result"]} ')
    print(f'P1 real answer : {part_one(read_file_lines("input.txt"))} expecting 1825')
    print("------------")
    print(f'P2 test case answer : {part_two(read_file_lines("test_input_2.txt"))}, expecting {TEST_CASE["p2_result"]} ')
    print(f'P2 real answer : {part_two(read_file_lines("input.txt"))} expecting 235200')
