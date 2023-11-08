from collections import deque, namedtuple


CrateMove = namedtuple('CraneMove', 'quantity, from_stack, to_stack')


def initialise_stacks(initial_stacks_description):
    initial_stacks = reversed(initial_stacks_description.splitlines())
    stack_names_line = next(initial_stacks)
    indices = slice(1, None, 4)  # just get significant characters with slice indexing (every 4 starting at 1)
    stacks = {stack_name: deque() for stack_name in stack_names_line[indices]}
    for line in initial_stacks:
        crates = line[indices]
        for crate, stack in zip(crates, stacks.values()):
            if crate != ' ':
                stack.append(crate)
    return stacks


class Crane:
    def rearrange_stacks(self, stacks, operations: list[CrateMove]):
        for crate_move in operations:
            self.move_crates(crate_move.quantity, stacks[crate_move.from_stack], stacks[crate_move.to_stack])

    def move_crates(self, quantity, from_stack, to_stack):
        pass


class Crane9000(Crane):
    def move_crates(self, quantity, from_stack, to_stack):
        for _ in range(quantity):
            to_stack.append(from_stack.pop())


class Crane9001(Crane):
    def move_crates(self, quantity, from_stack, to_stack):
        crane_load = reversed([from_stack.pop() for _ in range(quantity)])
        to_stack.extend(crane_load)


def top_crates(stacks):
    return ''.join(stack[-1] for stack in stacks.values())


def solve_problem(filename, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        initial_stacks_description, rearrangement_procedure = f.read().split('\n\n', 2)
        operations = list()
        for line in rearrangement_procedure.splitlines():
            _, quantity, _, from_stack, _, to_stack = line.split()
            operations.append(CrateMove(int(quantity), from_stack, to_stack))

    stacks = initialise_stacks(initial_stacks_description)
    crane = Crane9000()
    crane.rearrange_stacks(stacks, operations)
    result1 = top_crates(stacks)
    print(f"Part 1: top crates are {result1}")
    if expected1 is not None:
        assert result1 == expected1

    stacks = initialise_stacks(initial_stacks_description)
    crane = Crane9001()
    crane.rearrange_stacks(stacks, operations)
    result2 = top_crates(stacks)
    print(f"Part 2: top crates are {result2}")

    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 'CMZ', 'MCD')
    solve_problem('input.txt', 'MQSHJMWNH', 'LLWJRBHVZ')


if __name__ == '__main__':
    main()
