# https://adventofcode.com/2022/day/13
from common.read_input import read_file_lines

TEST_CASE = {
    "p1_result": 13,
    "p2_result": 140,

}


class SignalPair:
    def __init__(self, left: [], right: []):
        self.left: [] = left
        self.right: [] = right
        self.correct_order = False

    def __repr__(self):
        return f'LEFT: {self.left}   |   RIGHT: {self.right}'


def remove_outside_brackets(str_input_with_brackets: str) -> str:
    return str_input_with_brackets[1:-1]

#
# def parse_str_input(str_input: str) -> []:
#     result: [] = []
#     str_input = remove_outside_brackets(str_input)
#     if not str_input:
#         return result
#     split = str_input.split(',')
#     for sub_str in split:
#         if sub_str[0] == '[':
#             result.append(parse_str_input(sub_str))
#         else:
#             result.append(int(sub_str))
#     return result


# def parse_str_input(str_input: str) -> []:
#     result: [] | None = None
#     # str_input = remove_outside_brackets(str_input)
#     i = 0
#     current_num: str = ''
#     while i < len(str_input):
#         char = str_input[i]
#         if char == '[':
#             if not result:
#                 result = []
#             result.append(parse_str_input(str_input[1:]))
#             i = str_input.find(']') + 1
#         elif char == ']':
#             if current_num:
#                 result.append(int(current_num))
#             return result
#         elif char == ',':
#             result.append(int(current_num))
#             current_num = ''
#         else:
#             current_num += char
#         i += 1
#     return result


def compare_ints(lhs: int, rhs: int) -> int:
    if lhs < rhs:
        return 1
    elif lhs > rhs:
        return -1
    else:
        return 0


def compare_lists(lhs: [], rhs: []) -> int:
    left_len = len(lhs)
    right_len = len(rhs)
    for i in range(0, left_len):  # need to check rhs[i] exists
        if i >= right_len:  # left list is longer than right
            return -1
        if isinstance(lhs[i], list) and isinstance(rhs[i], list):
            list_res = compare_lists(lhs[i], rhs[i])
            if list_res != 0:
                return list_res
        elif isinstance(lhs[i], int) and isinstance(rhs[i], int):
            int_res = compare_ints(lhs[i], rhs[i])
            if int_res != 0:
                return int_res
        else:  # mixed type
            left = [lhs[i]] if isinstance(lhs[i], int) else lhs[i]
            right = [rhs[i]] if isinstance(rhs[i], int) else rhs[i]
            list_res = compare_lists(left, right)
            if list_res != 0:
                return list_res
    return 1 if right_len > left_len else 0


def check_order(sp: SignalPair):
    result = compare_lists(sp.left, sp.right)
    sp.correct_order = True if result > 0 else False  # a draw will be marked False


def part_one(my_input):
    my_signal_pairs: [SignalPair] = []
    for i in range(0, len(my_input), 3):
        left = eval(my_input[i])
        right = eval(my_input[i + 1])
        my_signal_pairs.append(SignalPair(left, right))

    correct_pair_indexes = []
    for i, signal_pair in enumerate(my_signal_pairs):
        check_order(signal_pair)
        if signal_pair.correct_order:
            correct_pair_indexes.append(i + 1)
    return sum(correct_pair_indexes)

# ---------------


def swap_positions(my_list: [], p1: int, p2: int):
    pair = my_list[p1], my_list[p2]
    my_list[p2], my_list[p1] = pair


def partition(signals: [], low: int, high: int) -> int:
    pivot = high
    i = low - 1
    for n in range(low, high - 1):
        left = signals[n]
        right = signals[pivot]
        if compare_lists(left, right) >= 0:
            i += 1
            swap_positions(signals, i, n)
    i += 1
    swap_positions(signals, i, high)
    return i


def quicksort(signals: [], low: int, high: int):
    if low >= high or low < 0:
        return
    partition_index = partition(signals, low, high)
    quicksort(signals, low, partition_index)
    quicksort(signals, partition_index + 1, high)


def quicksort2(signals: []):
    if len(signals) > 1:
        pivot = int(len(signals) / 2)
        val = signals[pivot]
        left = [i for i in signals if compare_lists(i, val) >= 0]
        # mid = [i for i in signals if compare_lists(i, val) == 0]
        right = [i for i in signals if compare_lists(i, val) < 0]
        result = quicksort2(left) + signals[pivot] + quicksort2(right)
        return result
    else:
        return signals


def part_two(my_input):
    my_signals = []
    for i in range(0, len(my_input), 3):
        my_signals.append(eval(my_input[i]))  # left
        my_signals.append(eval(my_input[i + 1]))  # right

    my_signals.append(eval("[[2]]"))
    my_signals.append(eval("[[6]]"))
    # quicksort2(my_signals)
    quicksort(my_signals, 0, len(my_signals) - 1)
    return 2


if __name__ == '__main__':
    # print(f'P1 test case answer : {part_one(read_file_lines("test_input.txt"))}, expecting {TEST_CASE["p1_result"]} ')
    # print(f'P1 real answer : {part_one(read_file_lines("input.txt"))} expecting 5825')
    # print("------------")
    print(f'P2 test case answer : {part_two(read_file_lines("test_input.txt"))}, expecting {TEST_CASE["p2_result"]} ')
    # print(f'P2 real answer : {part_two(read_file_lines("input.txt"))} expecting ?')
