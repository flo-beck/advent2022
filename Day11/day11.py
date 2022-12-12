# https://adventofcode.com/2022/day/11
import math
import re
from enum import Enum

from common.read_input import read_file_lines

TEST_CASE = {
    "p1_result": 10605,
    "p2_result": 2713310158,

}


class Op(Enum):
    ADD = '+'
    MULTI = '*'


class Amount(Enum):
    OLD = 1
    NEW = 2


class Monkey:
    def __init__(self, index: int, test_amount: int, worry_op: Op, worry_amount: Amount | int, true: int, false: int, max_mod: int):
        self.i: int = index
        self.test_amount: int = test_amount
        self.worry_op:  Op = worry_op
        self.worry_amount: Amount | int = worry_amount
        self.true_index: int = true
        self.false_index: int = false
        self.items: [int] = []
        self.inspect_total = 0
        self.max_mod = max_mod

    def do_operation(self, item_index: int) -> int:
        amount = self.items[item_index] if self.worry_amount == Amount.OLD else self.worry_amount
        match self.worry_op:
            case Op.MULTI:
                if self.max_mod != 0:
                    return (self.items[item_index] * amount) % self.max_mod
                return self.items[item_index] * amount
            case Op.ADD:
                if self.max_mod != 0:
                    return (self.items[item_index] + amount) % self.max_mod
                return self.items[item_index] + amount

    def do_worry_level_test(self, item_index) -> int:
        worry_amount = self.items[item_index]
        return self.true_index if worry_amount % self.test_amount == 0 else self.false_index

    def update_item_worry_level(self, item_index: int, new_worry_level: int):
        self.items[item_index] = new_worry_level

    def __repr__(self):
        return f'Monkey {self.i} inspected {self.inspect_total} items'
    # def __repr__(self):
    #     return f'Monkey {self.i} holds {len(self.items)} items: {self.items} - total [{self.inspect_total}]'


def parse_items(items_str: str) -> [int]:
    items = []
    split = items_str[18:].split(', ')
    for n in split:
        items.append(int(n))
    return items


def parse_operation(op_str: str) -> (Op, int | Amount):
    op: Op = Op(op_str[23:24])
    amount_str: str = op_str[25:]
    amount = Amount.OLD if amount_str == 'old' else int(amount_str)
    return op, amount


def parse_test(test_str: str) -> int:
    return int(test_str[21:])


def parse_test_result(result_str: str, test_type: bool) -> int:
    if test_type:
        return int(result_str[29:])
    else:
        return int(result_str[30:])


def parse_monkey_input(monkey_input: [str]) -> Monkey:
    index = int(monkey_input[0][7:8])
    items = parse_items(monkey_input[1])
    op, worry = parse_operation(monkey_input[2])
    test_amount = parse_test(monkey_input[3])
    true_index = parse_test_result(monkey_input[4], True)
    false_index = parse_test_result(monkey_input[5], False)
    monkey = Monkey(index, test_amount, op, worry, true_index, false_index, 0)
    monkey.items = items
    return monkey


def print_monkeys(monkeys: [Monkey]):
    for monkey in monkeys:
        print(f'{monkey}')


def get_worry_level_after_inspection(monkey: Monkey, item_index: int) -> int:
    item_worry_level = monkey.do_operation(item_index)  # monkey inspects item
    return math.floor(item_worry_level / 3)  # apply item-ok relief


def calc_monkey_business(monkeys: [Monkey]) -> int:
    most_active: Monkey | None = None
    second_most_active: Monkey | None = None
    for monkey in monkeys:
        if most_active is None or monkey.inspect_total > most_active.inspect_total:
            most_active = monkey
        elif second_most_active is None or monkey.inspect_total > second_most_active.inspect_total:
            second_most_active = monkey
    return most_active.inspect_total * second_most_active.inspect_total


def do_rounds_part_one(num_rounds: int, monkeys: [Monkey]) -> [Monkey]:
    for round_num in range(0, num_rounds):
        for monkey in monkeys:
            for item_index in range(0, len(monkey.items)):
                item_worry_level = get_worry_level_after_inspection(monkey, item_index)
                monkey.update_item_worry_level(item_index, item_worry_level)
                monkey.inspect_total += 1
                to_monkey_index = monkey.do_worry_level_test(item_index)
                monkeys[to_monkey_index].items.append(monkey.items[item_index])  # pass item to new monkey
            monkey.items = []                                                    # monkey has thrown all items
        print(f'ROUND {round_num + 1}')
        print_monkeys(monkeys)
        print(f'')
    return monkeys


def parse_monkeys(my_input) -> [Monkey]:
    monkeys: [Monkey] = []
    for i, line in enumerate(my_input):
        if re.match("Monkey ([0-9])", line):
            monkeys.append(parse_monkey_input(my_input[i:i + 6]))
        else:
            continue
    print(f'START')
    print_monkeys(monkeys)
    print(f'')
    return monkeys


def part_one(my_input):
    monkeys = parse_monkeys(my_input)
    monkeys = do_rounds_part_one(20, monkeys)
    return calc_monkey_business(monkeys)

# ---------------


def get_worry_level_after_inspection_part_two(monkey: Monkey, item_index: int) -> int:
    item_worry_level = monkey.do_operation(item_index)  # monkey inspects item
    return item_worry_level


def do_rounds_part_two(num_rounds: int, monkeys: [Monkey]) -> [Monkey]:
    for round_num in range(1, num_rounds + 1):
        for monkey in monkeys:
            for item_index in range(0, len(monkey.items)):
                item_worry_level = get_worry_level_after_inspection_part_two(monkey, item_index)
                monkey.update_item_worry_level(item_index, item_worry_level)
                monkey.inspect_total += 1
                to_monkey_index = monkey.do_worry_level_test(item_index)
                monkeys[to_monkey_index].items.append(monkey.items[item_index])  # pass item to new monkey
            monkey.items = []                                                    # monkey has thrown all items
        if round_num in [1, 20, 1000, 2000, 3000, 4000, 10000]:
            print(f'ROUND {round_num}')
            print_monkeys(monkeys)
            print(f'')
    return monkeys


def get_maxi_modulo(monkeys: [Monkey]) -> int:
    deciding_values = []
    for monkey in monkeys:
        deciding_values.append(monkey.test_amount)
    return math.prod(deciding_values)


def set_monkeys_maxi_modulo(monkeys: [Monkey], maxi_modulo: int):
    for monkey in monkeys:
        monkey.max_mod = maxi_modulo


def part_two(my_input):
    monkeys = parse_monkeys(my_input)
    maxi_modulo = get_maxi_modulo(monkeys)
    set_monkeys_maxi_modulo(monkeys, maxi_modulo)
    monkeys = do_rounds_part_two(10000, monkeys)
    return calc_monkey_business(monkeys)


if __name__ == '__main__':
    # print(f'P1 test case answer : {part_one(read_file_lines("test_input.txt"))}, expecting {TEST_CASE["p1_result"]} ')
    # print(f'P1 real answer : {part_one(read_file_lines("input.txt"))} expecting 56120')
    # print("------------")
    # print(f'P2 test case answer : {part_two(read_file_lines("test_input.txt"))}, expecting {TEST_CASE["p2_result"]} ')
    print(f'P2 real answer : {part_two(read_file_lines("input.txt"))} expecting 24389045529')
