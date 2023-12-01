from collections import deque, defaultdict
from itertools import count

from utilities.enums2 import IntEnumWithProperty


class Orientation(IntEnumWithProperty):
    N = 0, 0-1j
    NE = 1, 1-1j
    E = 2, 1+0j
    SE = 3, 1+1j
    S = 4, 0+1j
    SW = 5, -1+1j
    W = 6, -1+0j
    NW = 7, -1-1j

    @property
    def vector(self) -> complex:
        return self._property_

    @property
    def at_right(self) -> 'Orientation':
        return self.__class__((self + 1) % len(self.__class__))

    @property
    def at_left(self) -> 'Orientation':
        return self.__class__((self - 1) % len(self.__class__))


def do_round(elves, directions):
    """Move positions according to directions order
    returns True if moves occurred, False otherwise """
    destinations = defaultdict(deque)  # destination => from positions list
    all_neighbor_offsets = [orientation.vector for orientation in Orientation]
    for from_position in elves:
        if any(from_position + d in elves for d in all_neighbor_offsets):
            # elf has neighbors, she needs to move
            for direction, neighbor_offsets in directions:
                if not any(from_position + d in elves for d in neighbor_offsets):  # direction is free
                    destinations[from_position + direction].append(from_position)  # register and track conflicts
                    break

    destinations = {destination: from_positions[0]
                    for destination, from_positions in destinations.items()
                    if len(from_positions) == 1}  # keep only singles

    elves.difference_update(destinations.values())  # remove previous positions
    elves.update(destinations.keys())  # add new ones

    return bool(destinations)  # whether some elves moved


def do_rounds(elves, rounds=None):
    directions = deque((direction.vector, (direction.at_left.vector, direction.vector, direction.at_right.vector))
                       for direction in [Orientation.N, Orientation.S, Orientation.W, Orientation.E])
    round_iterator = range(rounds) if rounds is not None else count()
    for round_index in round_iterator:
        if do_round(elves, directions):
            directions.rotate(-1)
        else:
            return round_index + 1
    return rounds


def ground_covered(elves):
    width = max(p.real for p in elves) - min(p.real for p in elves) + 1
    height = max(p.imag for p in elves) - min(p.imag for p in elves) + 1
    return int(width * height - len(elves))


def solve_problem(filename, expected1=None, expected2=None):
    print(f'--------- {filename}')

    initial_elves = set()
    with open(filename) as f:
        for j, line in enumerate(f.read().splitlines()):
            initial_elves.update(complex(i, j) for i, char in enumerate(line) if char == '#')

    elves = set(initial_elves)
    do_rounds(elves, rounds=10)
    result1 = ground_covered(elves)
    print(f"Part 1: ground covered by elves is {result1}")
    if expected1 is not None:
        assert result1 == expected1

    elves = set(initial_elves)
    result2 = do_rounds(elves)
    print(f"Part 2: elves don't move after round {result2}")
    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 110, 20)
    solve_problem('input.txt', 4034, 960)


if __name__ == '__main__':
    main()
