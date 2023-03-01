from ast import literal_eval

from functools import cmp_to_key
from itertools import chain, dropwhile
from math import prod


def compare(left, right):
    if type(left) is type(right) is int:
        return left - right
    elif type(left) is type(right) is list:
        v = next(dropwhile(lambda c: c == 0, (compare(l, r) for (l, r) in zip(left, right))), 0)
        return v if v != 0 else len(left) - len(right)
    elif type(left) is int and type(right) is list:
        return compare([left], right)
    elif type(left) is list and type(right) is int:
        return compare(left, [right])
    else:
        return -1 if left < right else 0 if right == left else 1


def solve_problem(filename, expected1=None, expected2=None, testing=False):
    print(f'--------- {filename}')
    with open(filename) as f:
        packet_pairs = [tuple(literal_eval(line) for line in packet_pair_block.splitlines())
                        for packet_pair_block in f.read().split('\n\n')]

    if testing:
        for i, (p1, p2) in enumerate(packet_pairs):
            print(f"Pair {i+1} {'NOT ' if compare(p1, p2) > 0 else ''}in the right order")
            print(p1)
            print(p2)

    result1 = sum(i+1 for i, (p1, p2) in enumerate(packet_pairs) if compare(p1, p2) <= 0)

    print(f"Part 1: sum of right order pair indexes is {result1}")
    if expected1 is not None:
        assert result1 == expected1

    dividers = [[2]], [[6]]
    packets = list(chain(*packet_pairs, dividers))
    result2 = prod(sum(compare(packet, divider) < 0 for packet in packets) + 1 for divider in dividers)

    print(f"Part 2: decoder key is {result2}")
    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 13, 140, testing=True)
    solve_problem('input.txt', 6478, 21922)


if __name__ == '__main__':
    main()
