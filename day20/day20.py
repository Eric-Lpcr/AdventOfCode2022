from collections import deque, Counter

from utilities.itertools_recipes import ncycles


class Item:
    # This wrapper class has no __eq__ operator, so that instances with same value will differ
    # index() on list will check for object identity
    def __init__(self, value):
        self.value = value


def mix(numbers, times=1):
    items_list = [Item(value) for value in numbers]  # wrap number
    items_chain = deque(items_list)

    for item in ncycles(items_list, times):  # items_list keeps initial order
        item_index = items_chain.index(item)  # find the item, as it has moved with the previous ones
        items_chain.rotate(-item_index)  # item to move is now at left
        items_chain.popleft()  # remove it
        items_chain.rotate(-item.value)  # step to target position (deque implementation reduces to length modulo)
        items_chain.appendleft(item)  # and insert it back

    return [item.value for item in items_chain]


def sum_of_selected_numbers(numbers, indices):
    zero_position = numbers.index(0)
    return sum(numbers[(zero_position + rank) % len(numbers)] for rank in indices)


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        numbers = [int(line) for line in f.readlines()]

    mixed_numbers = mix(numbers)
    result1 = sum_of_selected_numbers(mixed_numbers, [1000, 2000, 3000])
    print(f"Part 1: grove coordinates sum is {result1}")
    if testing and expected1 is not None:
        assert result1 == expected1

    decryption_key = 811589153
    numbers2 = [n * decryption_key for n in numbers]
    mixed_numbers = mix(numbers2, times=10)
    result2 = sum_of_selected_numbers(mixed_numbers, [1000, 2000, 3000])
    print(f"Part 2: grove coordinates sum is {result2}")
    if testing and expected2 is not None:
        assert result2 == expected2


if __name__ == '__main__':
    main('test.txt', True, 3, 1623178306)
    main('input.txt', True, 11123, 4248669215955)
