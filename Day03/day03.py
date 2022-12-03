# https://adventofcode.com/2022/day/2
from enum import Enum

from common.read_input import read_file_lines

TEST_CASE = {
    "p1_result": 157,
    "p2_result": 70,
}


def find_common_item(lhs, rhs):
    for item in lhs:
        if rhs.find(item) >= 0:
            return item
    raise ValueError(f'No matching letters in strings {lhs} : {rhs}')


def calc_item_priority(item):
    lower_value = ord(str.lower(item)) - 96
    return lower_value if str.islower(item) else lower_value + 26


def part_one(my_input):
    total = 0
    for rucksack_contents in my_input:
        index = int(len(rucksack_contents)/2)
        left_compartment = rucksack_contents[0:index]
        right_compartment = rucksack_contents[index:]
        common_item = find_common_item(left_compartment, right_compartment)
        total += calc_item_priority(common_item)
    return total


# ---------------------

def find_badge(elf_group):
    return elf_group[0].intersection(elf_group[1], elf_group[2])
    # for item in elf_group[0]:
    #     if elf_group[1].find(item) >= 0 and elf_group[2].find(item) >= 0:
    #         return item
    # raise ValueError(f'No matching letters in elf_group {elf_group}')


def part_two(my_input):
    total = 0
    elf_group = []
    for line in my_input:
        elf_group.append(set(line))
        if len(elf_group) == 3:
            # We have our group of 3 elves (also could have used grouper (itertools) )
            badge = find_badge(elf_group).pop()
            total += calc_item_priority(badge)
            elf_group.clear()
    return total


if __name__ == '__main__':
    print(f'P1 test case answer : {part_one(read_file_lines("test_input.txt"))}, expecting {TEST_CASE["p1_result"]} ')
    print(f'P1 real answer : {part_one(read_file_lines("input.txt"))} expecting 8039')
    print("------------")
    print(f'P2 test case answer : {part_two(read_file_lines("test_input.txt"))}, expecting {TEST_CASE["p2_result"]} ')
    print(f'P2 real answer : {part_two(read_file_lines("input.txt"))} expecting 2510')
