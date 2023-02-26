from itertools import count

from dataclasses import dataclass


@dataclass
class NumberPosition:
    value: int
    position: int

    def __lt__(self, other):
        return self.position < other.position

    def __repr__(self):
        return f'{self.value} at {self.position}'


def mix(numbers):
    number_position = [NumberPosition(value, position) for value, position in zip(numbers, count())]
    modulo = len(number_position) - 1
    number_zero = None
    for index, number in enumerate(number_position):
        if number.value == 0:
            number_zero = number
            continue
        previous_position = number.position
        next_position = (previous_position + number.value) % modulo
        if previous_position < next_position:
            for i, n in enumerate(number_position):
                if i != index and previous_position < n.position <= next_position:
                    n.position -= 1
        else:
            for i, n in enumerate(number_position):
                if i != index and next_position <= n.position < previous_position:
                    n.position += 1
        number.position = next_position

    mixed_numbers = [number.value for number in sorted(number_position)]
    return mixed_numbers, number_zero.position


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        numbers = [int(line) for line in f.readlines()]

    mixed_numbers, zero_position = mix(numbers)
    selected_mixed_numbers = [mixed_numbers[(zero_position + rank) % len(mixed_numbers)] for rank in [1000, 2000, 3000]]
    result1 = sum(selected_mixed_numbers)
    print(f"Part 1: grove coordinates sum is {result1}")
    if testing and expected1 is not None:
        assert result1 == expected1

    result2 = 0
    print(f"Part 2: {result2}")
    if testing and expected2 is not None:
        assert result2 == expected2


if __name__ == '__main__':
    main('test.txt', True, 3, None)
    main('input.txt')
