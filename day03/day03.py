from functools import reduce
from itertools import zip_longest


def compute_item_priority(item):
    if item.islower():
        return ord(item) - ord('a') + 1  # 'a' gives 1
    else:
        return ord(item) - ord('A') + 1 + 26  # 'A' gives 27


def compute_rucksack_priority(rucksack):
    compartment_size = len(rucksack) // 2
    first_compartment = rucksack[:compartment_size]
    second_compartment = rucksack[compartment_size:]
    common_item = (set(first_compartment) & set(second_compartment)).pop()
    # print(f'Item {common_item} = {compute_item_priority(common_item)}')
    return compute_item_priority(common_item)


def compute_rucksacks_priorities(rucksacks):
    return map(compute_rucksack_priority, rucksacks)


def compute_rucksack_group_priority(rucksack_group):
    # badge = reduce(lambda badges, rucksack: badges.intersection(set(rucksack)),
    #                rucksack_group[1:],
    #                set(rucksack_group[0])
    #                ).pop()
    # set::intersection takes multiple sets
    rucksacks_sets = map(set, rucksack_group)
    badge = next(rucksacks_sets).intersection(*rucksacks_sets).pop()
    return compute_item_priority(badge)


def grouper(iterable, n, fill_value=None):
    """Collect data into fixed-length chunks or blocks"""
    """From https://docs.python.org/fr/3.8/library/itertools.html#itertools-recipes"""
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n  # Trick: same iterator n times, zip will take n items at each of its iterations
    return zip_longest(*args, fillvalue=fill_value)


def compute_rucksack_groups_priorities(rucksacks, group_size=3):
    return map(compute_rucksack_group_priority, grouper(rucksacks, group_size))


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        rucksacks = [line.strip() for line in f.readlines()]

    result1 = sum(compute_rucksacks_priorities(rucksacks))
    print(f"Part 1: sum of rucksacks priorities is {result1}")
    if testing and expected1 is not None:
        assert result1 == expected1

    result2 = sum(compute_rucksack_groups_priorities(rucksacks))
    print(f"Part 2: sum of rucksack groups priorities is {result2}")

    if testing and expected2 is not None:
        assert result2 == expected2


if __name__ == '__main__':
    main('test.txt', True, 157, 70)
    main('input.txt')
