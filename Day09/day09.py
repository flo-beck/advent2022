# https://adventofcode.com/2022/day/9

from common.read_input import read_file_lines

TEST_CASE = {
    "p1_result": 13,
    "p2_result": 36,

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


def move_tail(head_pos: (int, int), tail_pos: (int, int)) -> (int, int):
    diff_x = abs(head_pos[0] - tail_pos[0])
    diff_y = abs(head_pos[1] - tail_pos[1])
    if diff_x >= 2 or diff_y >= 2:
        return move_tail_towards_head(head_pos, tail_pos)
    else:
        return tail_pos


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

    return len(set(tail_positions))


# ---------------

def draw_grid(positions: [[(int, int)]], min_dimension: (int, int), max_dimension: (int, int)):
    for y in range(min_dimension[1], max_dimension[1]):
        for x in range(min_dimension[0], max_dimension[0]):
            char = "s" if x == 0 and y == 0 else "."
            for i in reversed(range(0, len(positions))):
                latest_pos = positions[i][-1]
                if latest_pos[0] == x and latest_pos[1] == y:
                    char = str(i) if i != 0 else "H"
            print(char, end='')
        print('')
    print('')
    print('')


def init_x_knots(num_knots: int) -> [[(int, int)]]:
    result = []
    for i in range(0, num_knots):
        result.append([get_init_position()])
    return result


def part_two(my_input):
    all_positions: [[(int, int)]] = init_x_knots(10)
    # draw_grid(all_positions, (-11, -15), (15, 5))
    tail_positions = [get_init_position()]

    for instruction in my_input:  # R 4
        split = instruction.split(' ')
        # print(f'{instruction}')
        for rep in range(0, int(split[1])):  # for each instruction
            # print(f'{instruction} - {rep + 1}')
            all_positions[0].append(move_head(split[0], all_positions[0][-1]))
            for i in range(1, len(all_positions)):  # for each knot
                all_positions[i].append(move_tail(all_positions[i - 1][-1], all_positions[i][-1]))
                if i == len(all_positions) - 1:  # i.e. the TAIL
                    tail_positions.append(all_positions[i][-1])
        # draw_grid(all_positions, (-12, -15), (15, 6))

    return len(set(tail_positions))


if __name__ == '__main__':
    print(f'P1 test case answer : {part_one(read_file_lines("test_input.txt"))}, expecting {TEST_CASE["p1_result"]} ')
    print(f'P1 real answer : {part_one(read_file_lines("input.txt"))} expecting 6745')
    print("------------")
    print(f'P2 test case answer : {part_two(read_file_lines("test_input_2.txt"))}, expecting {TEST_CASE["p2_result"]} ')
    print(f'P2 real answer : {part_two(read_file_lines("input.txt"))} expecting ?')
