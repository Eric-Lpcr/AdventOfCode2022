from collections import deque
from itertools import zip_longest


def solve_problem(filename, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        initial_stacks_description, rearrangement_procedure = f.read().split('\n\n', 2)

    initial_stacks = reversed(initial_stacks_description.splitlines())
    stack_count = max(int(stack_index) for stack_index in next(initial_stacks).split())
    stacks = [deque() for _ in range(stack_count)]
    for line in initial_stacks:
        for crate, stack in zip_longest(line[1::4], stacks, fillvalue=' '):
            if crate != ' ':
                stack.append(crate)

    for crane_move in rearrangement_procedure.splitlines():
        number, from_stack, to_stack = [int(x) for x in crane_move.split()[1::2]]
        stacks[to_stack-1].extend([stacks[from_stack-1].pop() for _ in range(number)])

    result1 = ''.join([stack[-1] for stack in stacks])
    print(f"Part 1: top crates are {result1}")
    if expected1 is not None:
        assert result1 == expected1

    result2 = 0
    print(f"Part 2: {result2}")

    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 'CMZ')
    solve_problem('input.txt', 'MQSHJMWNH')


if __name__ == '__main__':
    main()
