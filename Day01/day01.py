# https://adventofcode.com/2022/day/1
import string

from common.read_input import read_file_lines

TEST_CASE = {
    "p1_result": 24000,
    "p2_result": 45000,
}

SNACKIEST_ELF = {
    "elf_number": 0,
    "calories": 0
}


def part_one(my_input):
    current_calories = 0
    elf_count = 1
    for val in my_input:
        # if we reach the end of this elf's input
        if not val:
            if current_calories > SNACKIEST_ELF["calories"]:
                SNACKIEST_ELF["calories"] = current_calories
                SNACKIEST_ELF["elf_number"] = elf_count
            elf_count += 1
            current_calories = 0
        else:
            current_calories += int(val)
    print(f'Snackiest elf : {SNACKIEST_ELF["elf_number"]} with {SNACKIEST_ELF["calories"]} calories')
    return SNACKIEST_ELF["calories"]


SNACKIEST_ELVES = []


class Elf:
    def __init__(self, index: int, calories: int):
        self.index: int = index
        self.calories: int = calories

    def __repr__(self):
        return f'Elf {self.index} has {self.calories} calories'


def compare_snackiness(elf_num, calories):
    if len(SNACKIEST_ELVES) < 3:
        add_elf(elf_num, calories)
    else:
        for elf in SNACKIEST_ELVES:
            if calories > elf.calories:
                add_elf(elf_num, calories)
                break


def add_elf(elf_num, calories):
    SNACKIEST_ELVES.append(Elf(elf_num, calories))
    SNACKIEST_ELVES.sort(key=lambda elf: elf.calories, reverse=True)
    if len(SNACKIEST_ELVES) > 3:
        SNACKIEST_ELVES.pop()


def total_snackiest_calories():
    total = 0
    for elf in SNACKIEST_ELVES:
        total += elf.calories
    return total


def part_two(my_input):
    current_calories = 0
    elf_count = 1
    for val in my_input:
        # if we reach the end of this elf's input
        if not val:
            compare_snackiness(elf_count, current_calories)
            elf_count += 1
            current_calories = 0
        else:
            current_calories += int(val)
    compare_snackiness(elf_count, current_calories)
    print(SNACKIEST_ELVES)
    return total_snackiest_calories()


if __name__ == '__main__':
    print(f'P1 test case answer : {part_one(read_file_lines("test_input.txt"))}, expecting {TEST_CASE["p1_result"]} ')
    print(f'P1 real answer : {part_one(read_file_lines("input.txt"))}')
    print("------------")
    print(f'P2 test case answer : {part_two(read_file_lines("test_input.txt"))}, expecting {TEST_CASE["p2_result"]} ')
    print(f'P2 real answer : {part_two(read_file_lines("input.txt"))}')
