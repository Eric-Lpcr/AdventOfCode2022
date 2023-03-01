from collections import deque, namedtuple
from utilities.itertools_recipes import ncycles


def mix(numbers, times=1):
    Item = namedtuple('I', 'initial_index, value')  # keep initial position to allow unicity and lookup in items chain
    items_list = list(Item(i, value) for i, value in enumerate(numbers))
    items_chain = deque(items_list)
    modulo = len(numbers) - 1  # 6 steps in a list of 7 items returns back to the same neighbors

    for item in ncycles(items_list, times):
        item_index = items_chain.index(item)  # find the item, as it has moved with the previous ones
        items_chain.rotate(-item_index)  # item to move is now at left
        items_chain.popleft()  # remove it
        shift = item.value % modulo
        items_chain.rotate(-shift)  # step to target position
        items_chain.appendleft(item)  # and insert it back

    return [c.value for c in items_chain]


def sum_of_selected_numbers(numbers, indices):
    zero_position = numbers.index(0)
    return sum(numbers[(zero_position + rank) % len(numbers)] for rank in indices)


def solve_problem(filename, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        numbers = [int(line) for line in f.readlines()]

    mixed_numbers = mix(numbers)
    result1 = sum_of_selected_numbers(mixed_numbers, [1000, 2000, 3000])
    print(f"Part 1: grove coordinates sum is {result1}")
    if expected1 is not None:
        assert result1 == expected1

    decryption_key = 811589153
    numbers2 = [n * decryption_key for n in numbers]
    mixed_numbers = mix(numbers2, times=10)
    result2 = sum_of_selected_numbers(mixed_numbers, [1000, 2000, 3000])
    print(f"Part 2: grove coordinates sum is {result2}")
    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 3, 1623178306)
    solve_problem('input.txt', 11123, 4248669215955)


if __name__ == '__main__':
    main()
