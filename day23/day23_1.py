from collections import deque, defaultdict

from utilities.coordinates import Coordinate2, Box
from utilities.enums2 import IntEnumWithProperty
from utilities.itertools_recipes import first


class Orientation(IntEnumWithProperty):
    N = 0, Coordinate2(0, -1)
    NE = 1, Coordinate2(1, -1)
    E = 2, Coordinate2(1, 0)
    SE = 3, Coordinate2(1, 1)
    S = 4, Coordinate2(0, 1)
    SW = 5, Coordinate2(-1, 1)
    W = 6, Coordinate2(-1, 0)
    NW = 7, Coordinate2(-1, -1)

    @property
    def vector(self) -> Coordinate2:
        return self._property_

    @property
    def at_right(self) -> 'Orientation':
        return self.__class__((self + 1) % len(self.__class__))

    @property
    def at_left(self) -> 'Orientation':
        return self.__class__((self - 1) % len(self.__class__))


def bounding_box(elves):
    box = Box(first(elves))
    for position in elves:
        box.extend(position)
    return box


def print_grid(elves):
    box = bounding_box(elves)
    for y in range(box.lower.y - 1, box.upper.y + 2):
        for x in range(box.lower.y - 1, box.upper.y + 2):
            if Coordinate2(x, y) in elves:
                print('#', end='')
            else:
                print('.', end='')
        print()


def do_round(positions, directions):
    destinations = defaultdict(list)
    for position in positions:
        if any(position + orientation.vector in positions
               for orientation in Orientation):  # elf has neighbors, needs to move
            for direction in directions:
                if any(position + d.vector in positions
                       for d in [direction.at_left, direction, direction.at_right]):  # direction is blocked
                    continue
                else:
                    destinations[position + direction.vector].append(position)
                    break

    destinations = {destination: from_positions[0]
                    for destination, from_positions in destinations.items()
                    if len(from_positions) == 1}

    positions.difference_update(destinations.values())
    positions.update(destinations.keys())


def do_rounds(elves, rounds):
    directions = deque([Orientation.N, Orientation.S, Orientation.W, Orientation.E])
    for _ in range(rounds):
        do_round(elves, directions)
        directions.rotate(-1)


def ground_covered(elves):
    box = bounding_box(elves)
    return box.grid_volume - len(elves)


def solve_problem(filename, expected1=None, expected2=None):
    print(f'--------- {filename}')

    elves = set()
    with open(filename) as f:
        for y, line in enumerate(f.read().splitlines()):
            elves.update(Coordinate2(x, y) for x, c in enumerate(line) if c == '#')

    do_rounds(elves, rounds=10)
    result1 = ground_covered(elves)
    print(f"Part 1: ground covered by elves is {result1}")
    if expected1 is not None:
        assert result1 == expected1

    result2 = 0
    print(f"Part 2: {result2}")
    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 110)
    solve_problem('input.txt', 4034)


if __name__ == '__main__':
    main()
