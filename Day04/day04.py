# https://adventofcode.com/2022/day/4
from enum import Enum

from common.read_input import read_file_lines

TEST_CASE = {
    "p1_result": 2,
    "p2_result": 4,
}


class Section:
    def __init__(self, section: str):
        split = section.split('-')
        self.start: int = int(split[0])
        self.end: int = int(split[1])

    def __repr__(self):
        return f'Section : {self.start} to {self.end} '


def parse_sections(line: str) -> (Section, Section):
    split = line.split(',')
    return Section(split[0]), Section(split[1])


def section_is_covered(sec1: Section, sec2: Section) -> bool:
    # if the entirety of sec2 is covered by sec1
    return sec1.start <= sec2.start <= sec1.end and sec2.end <= sec1.end


def part_one(my_input):
    total = 0
    for line in my_input:
        sections = parse_sections(line)
        if section_is_covered(sections[0], sections[1]) or section_is_covered(sections[1], sections[0]):
            total += 1
    return total


# --------------


def sections_overlap(sec1: Section, sec2: Section) -> bool:
    return (sec1.start <= sec2.start <= sec1.end) or (sec1.start <= sec2.end <= sec1.end)


def part_two(my_input):
    total = 0
    for line in my_input:
        sections = parse_sections(line)
        if sections_overlap(sections[0], sections[1]) or sections_overlap(sections[1], sections[0]):
            total += 1
    return total


if __name__ == '__main__':
    print(f'P1 test case answer : {part_one(read_file_lines("test_input.txt"))}, expecting {TEST_CASE["p1_result"]} ')
    print(f'P1 real answer : {part_one(read_file_lines("input.txt"))} expecting 424')
    print("------------")
    print(f'P2 test case answer : {part_two(read_file_lines("test_input.txt"))}, expecting {TEST_CASE["p2_result"]} ')
    print(f'P2 real answer : {part_two(read_file_lines("input.txt"))} expecting 804')
