# https://adventofcode.com/2022/day/2
from enum import Enum

from common.read_input import read_file_lines

TEST_CASE = {
    "p1_result": 15,
    "p2_result": 12,
}


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Result(Enum):
    WIN = 6
    LOSE = 0
    DRAW = 3


COMPARE_SHAPES = {
    # tuple (WIN, LOSE)
    Shape.ROCK: (Shape.PAPER, Shape.SCISSORS),
    Shape.PAPER: (Shape.SCISSORS, Shape.ROCK),
    Shape.SCISSORS: (Shape.ROCK, Shape.PAPER)
}


def compare_shapes(s1: Shape, s2: Shape):
    if s1 == s2:
        return Result.DRAW
    elif COMPARE_SHAPES[s2][0] == s1:
        return Result.WIN
    else:
        return Result.LOSE


class Player:
    shape_dict = {
        "A": Shape.ROCK,
        "B": Shape.PAPER,
        "C": Shape.SCISSORS,
        "X": Shape.ROCK,
        "Y": Shape.PAPER,
        "Z": Shape.SCISSORS
    }

    def __init__(self, num: int):
        self.num: int = num
        self.scores = []
        self.total = 0
        self.shape: Shape = None

    def parse_shape(self, letter):
        self.shape = Player.shape_dict[letter]

    def set_score(self, func):
        score = func(self)
        self.total += score
        self.scores.append(score)
        self.shape = None

    def __repr__(self):
        return f'Player {self.num} has total {self.total} after {len(self.scores)} rounds'


def calc_draw(p: Player):
    return p.shape.value + Result.DRAW.value


def calc_win(p: Player):
    return p.shape.value + Result.WIN.value


def calc_lose(p: Player):
    return p.shape.value + Result.LOSE.value


class Game:
    def __init__(self, p1: Player, p2: Player):
        self.round = 0
        self.p1: Player = p1
        self.p2: Player = p2

    def play_round(self):
        self.round += 1
        result = compare_shapes(self.p1.shape, self.p2.shape)
        match result:
            case Result.DRAW:
                self.p1.set_score(calc_draw)
                self.p2.set_score(calc_draw)
            case Result.WIN:
                self.p1.set_score(calc_win)
                self.p2.set_score(calc_lose)
            case Result.LOSE:
                self.p1.set_score(calc_lose)
                self.p2.set_score(calc_win)

    def __repr__(self):
        return f'Current round {self.round} \n{self.p1} \n{self.p2}'


def part_one(my_input):
    g = Game(Player(1), Player(2))
    for line in my_input:
        g.p1.parse_shape(line[0])
        g.p2.parse_shape(line[-1])
        g.play_round()
        # print(g)
    return g.p2.total

# ------------------


ROUND_RESULT = {
    "X": Result.LOSE,
    "Y": Result.DRAW,
    "Z": Result.WIN
}


def choose_shape(desired_result, p1_shape: Shape):
    match desired_result:
        case Result.DRAW:
            return p1_shape
        case Result.WIN:
            return COMPARE_SHAPES[p1_shape][0]
        case Result.LOSE:
            return COMPARE_SHAPES[p1_shape][1]


def part_two(my_input):
    g = Game(Player(1), Player(2))
    for line in my_input:
        g.p1.parse_shape(line[0])
        g.p2.shape = choose_shape(ROUND_RESULT[line[-1]], g.p1.shape)
        g.play_round()
    return g.p2.total


if __name__ == '__main__':
    print(f'P1 test case answer : {part_one(read_file_lines("test_input.txt"))}, expecting {TEST_CASE["p1_result"]} ')
    print(f'P1 real answer : {part_one(read_file_lines("input.txt"))} expecting 15523')
    print("------------")
    print(f'P2 test case answer : {part_two(read_file_lines("test_input.txt"))}, expecting {TEST_CASE["p2_result"]} ')
    print(f'P2 real answer : {part_two(read_file_lines("input.txt"))} expecting 15702')
