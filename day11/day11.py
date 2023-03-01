from collections import deque

import operator
import re
from dataclasses import dataclass, field
from functools import partial
from itertools import islice
from operator import attrgetter
from typing import Deque


class Game:
    def __init__(self, shall_divide_worry_level=True):
        self.monkeys = list()
        self.shall_divide_worry_level = shall_divide_worry_level
        self.item_modulus = 1

    def add_monkey(self, monkey):
        self.monkeys.append(monkey)
        monkey.game = self
        self.item_modulus *= monkey.test.divisor

    def send_to_monkey(self, receiver, item):
        self.monkeys[receiver].receive_item(item)

    def play(self, turns=1):
        for _ in range(turns):
            for monkey in self.monkeys:
                monkey.play_turn()

    @property
    def monkey_business(self):
        first, second = islice(sorted(map(attrgetter('inspections'), self.monkeys), reverse=True), 2)
        return first * second


def square(x):
    return x * x


class DivisibleBy:
    def __init__(self, divisor):
        self.divisor = divisor

    def __call__(self, number):
        return number % self.divisor == 0


@dataclass
class Monkey:
    name: int
    items: Deque[int]
    operation: partial
    test: DivisibleBy
    receiver_if_true: int
    receiver_if_false: int
    game: Game = field(init=False)
    inspections: int = 0

    def receive_item(self, item):
        self.items.append(item)

    def play_turn(self):
        while len(self.items):
            self.inspections += 1
            item = self.items.popleft()
            item = self.operation(item)
            if self.game.shall_divide_worry_level:
                item //= 3
            else:
                item %= self.game.item_modulus
            receiver = self.receiver_if_true if self.test(item) else self.receiver_if_false
            self.game.send_to_monkey(receiver, item)


def decode_monkey(description):
    pattern = re.compile(r'Monkey (?P<id>\d+):'
                         r'\s+Starting items: (?P<items>\d+(,\s\d+)*)'
                         r'\s+Operation: new = (?P<op1>(\d+)|(old)) (?P<op>[*+]) (?P<op2>(\d+)|(old))'
                         r'\s+Test: divisible by (?P<divisor>\d+)'
                         r'\s+If true: throw to monkey (?P<receiver_if_true>\d+)'
                         r'\s+If false: throw to monkey (?P<receiver_if_false>\d+)')

    match = pattern.match(description.replace('\n', ' '))
    monkey_index = int(match.group('id'))
    items = deque(int(item) for item in match.group('items').split(', '))

    op1 = match.group('op1')
    op = match.group('op')
    op2 = match.group('op2')
    operation = None
    if op1 == op2 == 'old' and op == '*':
        operation = square
    else:
        if op == '*':
            fct = operator.mul
        else:  # op == '+'
            fct = operator.add
        if op1 == 'old':
            operation = partial(fct, int(op2))
        elif op2 == 'old':
            operation = partial(fct, int(op1))
    test = DivisibleBy(int(match.group('divisor')))
    receiver_if_true = int(match.group('receiver_if_true'))
    receiver_if_false = int(match.group('receiver_if_false'))

    return Monkey(monkey_index, items, operation, test, receiver_if_true, receiver_if_false)


def solve_problem(filename, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        monkey_descriptions = f.read().split('\n\n')

    game = Game()
    for monkey_description in monkey_descriptions:
        game.add_monkey(decode_monkey(monkey_description))
    game.play(turns=20)

    result1 = game.monkey_business
    print(f"Part 1: monkey business is {result1}")
    if expected1 is not None:
        assert result1 == expected1

    game = Game(shall_divide_worry_level=False)
    for monkey_description in monkey_descriptions:
        game.add_monkey(decode_monkey(monkey_description))
    game.play(turns=10000)

    result2 = game.monkey_business
    print(f"Part 2: monkey business is {result2}")
    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 10605, 2713310158)
    solve_problem('input.txt', 88208, 21115867968)


if __name__ == '__main__':
    main()
