from collections import deque, namedtuple
from itertools import zip_longest


CraneMove = namedtuple('CraneMove', 'number, from_stack, to_stack')


def initialise_stacks(initial_stacks_description):
    initial_stacks = reversed(initial_stacks_description.splitlines())
    stack_count = max(int(stack_index) for stack_index in next(initial_stacks).split())
    stacks = [deque() for _ in range(stack_count)]
    for line in initial_stacks:
        crates = line[1::4]  # just get significant characters with [1::4] indexing (every 4 starting at 1)
        for crate, stack in zip_longest(crates, stacks, fillvalue=' '):
            if crate != ' ':
                stack.append(crate)
    return stacks


def rearrange(stacks, crane_moves, crane_model=9000):
    for crane_move in crane_moves:
        crane_load = [stacks[crane_move.from_stack-1].pop() for _ in range(crane_move.number)]
        if crane_model == 9001:
            crane_load = reversed(crane_load)
        stacks[crane_move.to_stack-1].extend(crane_load)


def top_crates(stacks):
    return ''.join(stack[-1] for stack in stacks)


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        initial_stacks_description, rearrangement_procedure = f.read().split('\n\n', 2)
        crane_moves = list()
        for line in rearrangement_procedure.splitlines():
            number, from_stack, to_stack = [int(x) for x in line.split()[1::2]]
            crane_moves.append(CraneMove(number, from_stack, to_stack))

    stacks = initialise_stacks(initial_stacks_description)
    rearrange(stacks, crane_moves, crane_model=9000)
    result1 = top_crates(stacks)
    print(f"Part 1: top crates are {result1}")
    if testing and expected1 is not None:
        assert result1 == expected1

    stacks = initialise_stacks(initial_stacks_description)
    rearrange(stacks, crane_moves, crane_model=9001)
    result2 = top_crates(stacks)
    print(f"Part 2: top crates are {result2}")

    if testing and expected2 is not None:
        assert result2 == expected2


if __name__ == '__main__':
    main('test.txt', True, 'CMZ', 'MCD')
    main('input.txt')
