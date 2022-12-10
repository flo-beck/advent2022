# https://adventofcode.com/2022/day/10
import math
from enum import Enum

from common.read_input import read_file_lines

TEST_CASE = {
    "p1_result": 13140,
    "p2_result": 'display groups of 2-6 from top',

}


class IType(Enum):
    ADDX = "addx"
    NOOP = "noop"


class Instruction:
    def __init__(self, my_str: str):
        split = my_str.split(" ")
        self.type: IType = IType(split[0]) if len(split) > 0 else IType.NOOP
        self.value: int = int(split[1]) if self.type == IType.ADDX else 0
        self.cycles_to_complete: int = 2 if self.type == IType.ADDX else 1

    def __repr__(self):
        return f'{self.type.name} {self.value}'


class Pixel:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Screen:
    def __init__(self):
        self.pixels: [[str]] = []
        for y in range(0, 6):
            row = []
            for x in range(0, 40):
                # row.append('.')
                row.append(' ')
            self.pixels.append(row)

    def draw_pixel(self, pixel_num: int, sprite_pos: int):
        pixel_index = pixel_num - 1
        pixel_x_pos = pixel_index % 40 if pixel_index >= 40 else pixel_index
        pixel_to_draw = Pixel(pixel_x_pos, math.floor(pixel_index / 40))
        sprite_centre = sprite_pos % 40 if sprite_pos >= 40 else sprite_pos
        if sprite_centre - 1 <= pixel_to_draw.x <= sprite_centre + 1:
            self.pixels[pixel_to_draw.y][pixel_to_draw.x] = '█'
            # self.pixels[pixel_to_draw.y][pixel_to_draw.x] = '#'

    def print(self):
        for y in range(0, len(self.pixels)):
            for x in range(0, len(self.pixels[0])):
                print(self.pixels[y][x], end='')
            print('')


class Cpu:
    def __init__(self, instructions: [Instruction]):
        self.cycle: int = 0
        self.instructions: [Instruction] = instructions
        self.curr_instruction: Instruction | None = None
        self.cycles_per_instruction: int = 0
        self.x_register: int = 1
        self.signal_strengths = []
        self.screen: Screen = Screen()

    def end_instruction(self):
        self.cycles_per_instruction = 0
        self.curr_instruction = None

    def start_cycle(self):
        self.cycle += 1
        if self.curr_instruction is None:
            self.curr_instruction = self.instructions.pop(0)
        return 1

    def do_cycle(self):
        if self.start_cycle() > 0:
            self.cycles_per_instruction += 1
            self.screen.draw_pixel(self.cycle, self.x_register)
            if self.cycle in [20, 60, 100, 140, 180, 220]:
                self.signal_strengths.append(self.cycle * self.x_register)
            if self.cycles_per_instruction == self.curr_instruction.cycles_to_complete:
                self.x_register += self.curr_instruction.value
                self.end_instruction()

    def run_cycles(self):
        while 1:
            if self.curr_instruction is not None or len(self.instructions) > 0:
                self.do_cycle()
                # print(self)
            else:
                break

    def __repr__(self):
        if self.curr_instruction is not None:
            return f'Cycle {self.cycle}: [X] = {self.x_register} ({self.curr_instruction} on ' \
                   f'{self.cycles_per_instruction}/{self.curr_instruction.cycles_to_complete})'
        elif len(self.instructions) > 0:
            return f'Cycle {self.cycle}: [X] = {self.x_register} Next: ({self.instructions[0]})'
        else:
            return f'Cycle {self.cycle}: [X] = {self.x_register} No instructions left'


def parse_instructions(my_input) -> [Instruction]:
    instructions = []
    for line in my_input:
        instructions.append(Instruction(line))
    return instructions


def part_one(my_input):
    instructions = parse_instructions(my_input)
    my_cpu = Cpu(instructions)
    my_cpu.run_cycles()
    print(f'{my_cpu.signal_strengths}')
    return sum(my_cpu.signal_strengths)

# ---------------


def part_two(my_input):
    instructions = parse_instructions(my_input)
    my_cpu = Cpu(instructions)
    my_cpu.run_cycles()
    my_cpu.screen.print()
    return sum(my_cpu.signal_strengths)


if __name__ == '__main__':
    print(f'P1 test case answer : {part_one(read_file_lines("test_input.txt"))}, expecting {TEST_CASE["p1_result"]} ')
    print(f'P1 real answer : {part_one(read_file_lines("input.txt"))} expecting 13920')
    print("------------")
    print(f'P2 test case answer : {part_two(read_file_lines("test_input.txt"))}, expecting {TEST_CASE["p2_result"]} ')
    print(f'P2 real answer : {part_two(read_file_lines("input.txt"))} expecting display letters [EGLHBLFJ]')
