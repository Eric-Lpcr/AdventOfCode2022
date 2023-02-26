import operator
import re


class Monkey:
    tribe = dict()
    operators = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}

    def __init__(self, name, value, left=None, op=None, right=None):
        self.name = name
        self.tribe[self.name] = self
        self.value = value
        self.left = left
        self.operator = self.operators.get(op)
        self.right = right

    def yell(self):
        if self.operator:
            return self.operator(self.tribe[self.left].yell(), self.tribe[self.right].yell())
        else:
            return self.value


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        pattern1 = re.compile(r'(\w{4}): (\d+)')
        pattern2 = re.compile(r'(\w{4}): (\w{4}) ([+*/-]) (\w{4})')
        for line in f.readlines():
            match1 = pattern1.match(line.strip())
            if match1:
                Monkey(match1.group(1), int(match1.group(2)))
            else:
                match2 = pattern2.match(line.strip())
                Monkey(match2.group(1), None, match2.group(2), match2.group(3), match2.group(4))
    tribe = Monkey.tribe

    result1 = tribe.get('root').yell()
    print(f"Part 1: root monkey value is {int(result1)}")
    if testing and expected1 is not None:
        assert result1 == expected1

    result2 = 0
    print(f"Part 2: {result2}")
    if testing and expected2 is not None:
        assert result2 == expected2


if __name__ == '__main__':
    main('test.txt', True, 152, None)
    main('input.txt', True, 10037517593724, None)
