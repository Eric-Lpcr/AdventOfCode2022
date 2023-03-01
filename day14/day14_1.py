from collections import namedtuple
from itertools import pairwise, chain

Coordinate = namedtuple('Coordinate', 'x, y')


class Cave:
    def __init__(self):
        self.rocks = set()  # Coordinates
        self.sand = set()  # Coordinates
        self.top = dict()  # key is x, value = min y
        self.bottom = 0  # max y

    def fill(self, sand_start=Coordinate(500, 0)):
        self.top = dict((x, min(c.y for c in chain(self.rocks, self.sand) if c.x == x))
                        for x in set(p.x for p in chain(self.rocks, self.sand)))
        self.bottom = max(c.y for c in chain(self.rocks, self.sand))
        previous_sand = len(self.sand)
        while self.drop_sand(sand_start):
            pass
        return len(self.sand) - previous_sand

    def drop_sand(self, position):
        if position in self.sand or position in self.rocks:
            return False
        x, y = position
        if x in self.top and y < self.top[x]:
            y = self.top[x] - 1
        while y < self.bottom:
            moved = False
            for dx in [0, -1, 1]:
                next_position = Coordinate(x + dx, y + 1)
                if not (next_position in self.sand or next_position in self.rocks):
                    x, y = next_position
                    moved = True
                    break
            if not moved:
                self.sand.add(Coordinate(x, y))
                if x in self.top and y < self.top[x] or x not in self.top:
                    self.top[x] = y
                return True
        return False


def all_between(start, stop):
    step = 1 if start <= stop else -1
    return range(start, stop + step, step)


def decode_path(rock_path):
    edges = (Coordinate(*map(int, edge_str.split(',', 2))) for edge_str in rock_path.split(' -> '))
    rocky_cells = set()
    for edge1, edge2 in pairwise(edges):
        rocky_cells.update(Coordinate(x, y)
                           for x in all_between(edge1.x, edge2.x)
                           for y in all_between(edge1.y, edge2.y))
    return rocky_cells


def solve_problem(filename, expected1=None, expected2=None):
    print(f'--------- {filename}')

    cave = Cave()
    with open(filename) as f:
        for rock_path in f.readlines():
            cave.rocks.update(decode_path(rock_path.strip()))

    result1 = cave.fill(Coordinate(500, 0))
    print(f"Part 1: quantity of sand added is {result1}")
    if expected1 is not None:
        assert result1 == expected1

    result2 = 0
    print(f"Part 2: {result2}")
    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 24)
    solve_problem('input.txt', 745)


if __name__ == '__main__':
    main()
