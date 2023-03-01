import math
import operator
import re


class Monkey:
    tribe = dict()

    def __init__(self, name):
        self.name = name
        self.tribe[self.name] = self


class BasicMonkey(Monkey):

    def __init__(self, name, value):
        super().__init__(name)
        self.value = value

    @property
    def yell(self):
        return self.value

    def __str__(self):
        return f'{self.name}: {self.value}'


class SmartMonkey(BasicMonkey):
    operators = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
    }

    def __init__(self, name, left, op, right):
        super().__init__(name, None)
        self.left = left
        self.operator = self.operators.get(op)
        self.right = right

    @property
    def yell(self):
        if self.operator:
            self.value = self.operator(self.tribe.get(self.left).yell, self.tribe.get(self.right).yell)
        return self.value


class Human(BasicMonkey):
    def __init__(self, name):
        super().__init__(name, None)
        self._solve()

    def _solve(self):
        self.value = math.nan
        current = self.tribe.get('root')
        while current is not self:
            right, left = self.tribe.get(current.right), self.tribe.get(current.left)
            right_yell, left_yell = right.yell, left.yell
            if math.isnan(right_yell):
                right.value = solve_right(current.value, current.operator, left_yell)
                current = right
            elif math.isnan(left_yell):
                left.value = solve_left(current.value, current.operator, right_yell)
                current = left
            else:
                raise RuntimeError('Can''t reach me in hierarchy')


def solve_right(result, op, left):
    if op is operator.eq:
        right = left
    elif op is operator.add:
        right = result - left
    elif op is operator.sub:
        right = left - result
    elif op is operator.mul:
        right = result / left
    elif op is operator.truediv:
        right = left / result
    else:
        right = None
    return right


def solve_left(result, op, right):
    if op is operator.eq:
        left = right
    elif op is operator.add:
        left = result - right
    elif op is operator.sub:
        left = result + right
    elif op is operator.mul:
        left = result / right
    elif op is operator.truediv:
        left = result * right
    else:
        left = None
    return left


def solve_problem(filename, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        operators = ''.join('\\' + op for op in SmartMonkey.operators.keys())
        pattern = re.compile(rf'''(?P<name>\w+): \s* ( 
                    (?P<value>\d+) 
                    | (?P<left>\w+) \s* (?P<op>[{operators}]) \s* (?P<right>\w+) )''', re.VERBOSE)
        for line in f.readlines():
            match = pattern.match(line)
            if match.group('value'):
                BasicMonkey(match.group('name'), int(match.group('value')))
            else:
                SmartMonkey(*match.group('name', 'left', 'op', 'right'))
    tribe = Monkey.tribe
    root = tribe.get('root')

    result1 = int(root.yell)
    print(f"Part 1: root monkey yell {result1}")
    if expected1 is not None:
        assert result1 == expected1

    root.operator = operator.eq
    root.value = True
    human = Human('humn')
    result2 = int(human.yell)
    print(f"Part 2: human shall yell {result2}")
    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 152, 301)
    solve_problem('input.txt', 10037517593724, 3272260914328)


if __name__ == '__main__':
    main()
