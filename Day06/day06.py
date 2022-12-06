# https://adventofcode.com/2022/day/6

from common.read_input import read_file

TEST_CASE = {
    "p1_1_test": "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
    "p1_2_test": "bvwbjplbgvbhsrlpgdmjqwftvncz",
    "p1_3_test": "nppdvjthqldpwncqszvftbrmjlhg",
    "p1_4_test": "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
    "p1_5_test": "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
    "p1_1_result": 7,
    "p1_2_result": 5,
    "p1_3_result": 6,
    "p1_4_result": 10,
    "p1_5_result": 11,
    "p2_1_result": 19,
    "p2_2_result": 23,
    "p2_3_result": 23,
    "p2_4_result": 29,
    "p2_5_result": 26,
}


def find_len_of_buffer_and_marker(input_str: str, marker_len: int) -> int:
    for i in range(len(input_str)):
        if i < marker_len - 1:
            continue
        else:
            marker = set(input_str[i - (marker_len - 1): i + 1])
            if len(marker) == marker_len:
                return i + 1
    raise ValueError(f'No marker of {marker_len} unique consecutive letters found')


# def part_one(my_input):
#     for i, letter in enumerate(my_input):
#         if i < 3:
#             continue
#         else:
#             last_four = set(my_input[i-3:i+1])
#             if len(last_four) == 4:
#                 return i + 1
#     raise ValueError(f'No marker of four different consecutive letters found')


def part_one(my_input):
    return find_len_of_buffer_and_marker(my_input, 4)

# ---------------


def part_two(my_input):
   return find_len_of_buffer_and_marker(my_input, 14)


if __name__ == '__main__':
    print(f'P1 test case answer : {part_one(TEST_CASE["p1_1_test"])}, expecting {TEST_CASE["p1_1_result"]} ')
    print(f'P1 test case answer : {part_one(TEST_CASE["p1_2_test"])}, expecting {TEST_CASE["p1_2_result"]} ')
    print(f'P1 test case answer : {part_one(TEST_CASE["p1_3_test"])}, expecting {TEST_CASE["p1_3_result"]} ')
    print(f'P1 test case answer : {part_one(TEST_CASE["p1_4_test"])}, expecting {TEST_CASE["p1_4_result"]} ')
    print(f'P1 test case answer : {part_one(TEST_CASE["p1_5_test"])}, expecting {TEST_CASE["p1_5_result"]} ')
    print(f'P1 real answer : {part_one(read_file("input.txt"))} expecting 1702')
    print("------------")
    print(f'P2 test case answer : {part_two(TEST_CASE["p1_1_test"])}, expecting {TEST_CASE["p2_1_result"]} ')
    print(f'P2 test case answer : {part_two(TEST_CASE["p1_2_test"])}, expecting {TEST_CASE["p2_2_result"]} ')
    print(f'P2 test case answer : {part_two(TEST_CASE["p1_3_test"])}, expecting {TEST_CASE["p2_3_result"]} ')
    print(f'P2 test case answer : {part_two(TEST_CASE["p1_4_test"])}, expecting {TEST_CASE["p2_4_result"]} ')
    print(f'P2 test case answer : {part_two(TEST_CASE["p1_5_test"])}, expecting {TEST_CASE["p2_5_result"]} ')
    print(f'P2 real answer : {part_two(read_file("input.txt"))} expecting 3559')
