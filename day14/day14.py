from collections import namedtuple
from itertools import pairwise, chain

Coordinate = namedtuple('Coordinate', 'x, y')


class Cave:
    def __init__(self,):
        self.rock = set()  # Coordinates
        self.sand = set()  # Coordinates
        self.top = dict()  # key is x, value = min y
        self.bottom = 0  # max y
        self.infinite_bottom_depth = None

    def at(self, position):
        if position in self.sand:
            return 'S'
        if self.infinite_bottom_depth and position.y == self.bottom or position in self.rock:
            return 'R'
        return None

    def fill(self, sand_start=Coordinate(500, 0)):
        for position in chain(self.rock, self.sand):
            self.update_top(position)
        self.bottom = max(position.y for position in chain(self.rock, self.sand))
        if self.infinite_bottom_depth:
            self.bottom += self.infinite_bottom_depth

        drop_count = 0
        while self.drop_sand(sand_start):
            drop_count += 1
        return drop_count

    def update_top(self, position):
        top = self.top.get(position.x)
        if top and position.y < top or top is None:
            self.top[position.x] = position.y

    def add_sand(self, position):
        self.sand.add(position)
        self.update_top(position)

    def fall_to_top(self, from_position):
        top = self.top.get(from_position.x, self.bottom)
        return Coordinate(from_position.x, max(from_position.y, top - 1))

    def drop_sand(self, position):
        if self.at(position) is not None:
            return False  # filled
        position = self.fall_to_top(position)

        while position.y < self.bottom:
            for dx in [0, -1, 1]:
                next_position = Coordinate(position.x + dx, position.y + 1)
                if self.at(next_position) is None:
                    position = next_position
                    break
            else:
                self.add_sand(position)
                return True  # rest
        return False  # flow out


def all_between(start, stop):
    step = 1 if start <= stop else -1
    return range(start, stop + step, step)


def decode_path(rock_path):
    edges = (Coordinate(*map(int, edge_str.split(',', 2))) for edge_str in rock_path.split(' -> '))
    rocky_cells = set()
    for (x1, y1), (x2, y2) in pairwise(edges):
        rocky_cells.update(Coordinate(x, y)
                           for x in all_between(x1, x2)
                           for y in all_between(y1, y2))
    return rocky_cells


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    cave = Cave()
    with open(filename) as f:
        for rock_path in f.readlines():
            cave.rock.update(decode_path(rock_path.strip()))

    result1 = cave.fill(Coordinate(500, 0))
    print(f"Part 1: quantity of sand added is {result1}")
    if testing and expected1 is not None:
        assert result1 == expected1

    cave.sand.clear()
    cave.infinite_bottom_depth = 2
    result2 = cave.fill(Coordinate(500, 0))
    print(f"Part 2: quantity of sand added is {result2}")
    if testing and expected2 is not None:
        assert result2 == expected2


if __name__ == '__main__':
    main('test.txt', True, 24, None)
    main('input.txt')
