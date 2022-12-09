# https://adventofcode.com/2022/day/9

from common.read_input import read_file_lines

TEST_CASE = {
    "p1_result": 13,
    "p2_result": 8,

}


def move_head(direction: str, current_position: (int, int)) -> (int, int):
    match direction:
        case "R":
            return current_position[0] + 1, current_position[1]
        case "U":
            return current_position[0], current_position[1] - 1
        case "L":
            return current_position[0] - 1, current_position[1]
        case "D":
            return current_position[0], current_position[1] + 1


def get_coord_change(h_coord: int, t_coord: int) -> int:
    result = t_coord
    if h_coord != t_coord:
        if h_coord > t_coord:
            result += 1
        else:
            result -= 1
    return result


def move_tail_towards_head(head_pos: (int, int), tail_pos: (int, int)) -> (int, int):
    x = get_coord_change(head_pos[0], tail_pos[0])
    y = get_coord_change(head_pos[1], tail_pos[1])
    return x, y


def move_tail(hp: (int, int), tp: (int, int)) -> (int, int):
    diff_x = abs(hp[0] - tp[0])
    diff_y = abs(hp[1] - tp[1])
    if diff_x >= 2 or diff_y >= 2:
        return move_tail_towards_head(hp, tp)
    else:
        return tp


def print_positions(head, tail):
    for i in range(0, len(head)):
        print(f'HEAD: [{head[i]}] TAIL: [{tail[i]}]')


def get_init_position() -> (int, int):
    return 0, 0


def part_one(my_input):
    head_positions: [(int, int)] = [get_init_position()]
    tail_positions: [(int, int)] = [get_init_position()]

    for instruction in my_input:  # R 4
        split = instruction.split(' ')
        for rep in range(0, int(split[1])):
            head_positions.append(move_head(split[0], head_positions[-1]))
            tail_positions.append(move_tail(head_positions[-1], tail_positions[-1]))
    # print(f'HEAD len : {len(head_positions)}  TAIL len: {len(tail_positions)}')
    # print_positions(head_positions, tail_positions)

    return len(set(tail_positions))


# ---------------


# def part_two(my_input):
#     return 2


if __name__ == '__main__':
    print(f'P1 test case answer : {part_one(read_file_lines("test_input.txt"))}, expecting {TEST_CASE["p1_result"]} ')
    print(f'P1 real answer : {part_one(read_file_lines("input.txt"))} expecting 6745')
    # print("------------")
    # print(f'P2 test case answer : {part_two(read_file_lines("test_input.txt"))}, expecting {TEST_CASE["p2_result"]} ')
    # print(f'P2 real answer : {part_two(read_file_lines("input.txt"))} expecting ?')
