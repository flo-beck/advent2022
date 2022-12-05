# https://adventofcode.com/2022/day/5
from collections import deque

# Try using a deque from collections - append is supposed to be faster than on a list

from common.read_input import read_file_lines

TEST_CASE = {
    "p1_result": 'CMZ',
    "p2_result": 'MCD',
}


class Instruction:
    def __init__(self, line: str):
        split = line.split(' ')
        self.num_to_move: int = int(split[1])
        self.from_stack: int = int(split[3])
        self.to_stack: int = int(split[5])

    def __repr__(self):
        return f'Instruction : move {self.num_to_move} from {self.from_stack} to {self.to_stack} '


def parse_input(my_input: []) -> ([], []):
    drawing_part = []
    instructions = []
    instructions_flag = False
    for line in my_input:
        if not line:
            instructions_flag = True
        elif not instructions_flag:
            drawing_part.append(line)
        else:
            instructions.append(Instruction(line))
    drawing_part.reverse()
    return drawing_part, instructions


def create_stacks(drawing: []) -> []:
    stacks = []
    num_stacks = len(drawing.pop(0).replace(" ", ""))
    for i in range(num_stacks):
        stacks.append(deque())
    for row in drawing:
        chunks = [row[i:i+4] for i in range(0, len(row), 4)]
        for i, chunk in enumerate(chunks):
            if chunk[0] == '[':
                stacks[i].append(chunk[1])
    return stacks


def find_longest_stack(stacks):
    longest = 0
    for stack in stacks:
        longest = len(stack) if len(stack) > longest else longest
    return longest


def print_stacks(stacks):
    n = find_longest_stack(stacks)
    for i in range(n):
        for stack in stacks:
            if len(stack) > i:
                print(f'[{stack[i]}] ', end='')
            else:
                print("    ", end='')
        print("")


def do_instructions(stacks: [], instructions: []):
    for instruction in instructions:
        for i in range(instruction.num_to_move):
            crate_to_move = stacks[instruction.from_stack - 1].pop()
            stacks[instruction.to_stack - 1].append(crate_to_move)


def read_stacks(stacks):
    result = ""
    for stack in stacks:
        result += stack[len(stack) - 1]
    return result


def part_one(my_input):
    drawing, instructions = parse_input(my_input)
    stacks = create_stacks(drawing)
    do_instructions(stacks, instructions)
    return read_stacks(stacks)


# --------------


def do_instructions_retaining_order(stacks: [], instructions: []):
    for instruction in instructions:
        crates_to_move = deque()
        for i in range(instruction.num_to_move):
            crates_to_move.appendleft(stacks[instruction.from_stack - 1].pop())
        stacks[instruction.to_stack - 1].extend(crates_to_move)


def part_two(my_input):
    drawing, instructions = parse_input(my_input)
    stacks = create_stacks(drawing)
    do_instructions_retaining_order(stacks, instructions)
    return read_stacks(stacks)


if __name__ == '__main__':
    print(f'P1 test case answer : {part_one(read_file_lines("test_input.txt"))}, expecting {TEST_CASE["p1_result"]} ')
    print(f'P1 real answer : {part_one(read_file_lines("input.txt"))} expecting ZWHVFWQWW')
    print("------------")
    print(f'P2 test case answer : {part_two(read_file_lines("test_input.txt"))}, expecting {TEST_CASE["p2_result"]} ')
    print(f'P2 real answer : {part_two(read_file_lines("input.txt"))} expecting ?')
