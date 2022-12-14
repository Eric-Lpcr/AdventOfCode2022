from itertools import pairwise, chain


class Cave:
    def __init__(self,):
        self.rock = set()
        self.sand = set()
        self.top = dict()  # key is x, value = min y
        self.bottom = 0  # max y
        self.infinite_bottom_depth = None

    def at(self, position):
        if position in self.sand:
            return 'S'
        if self.infinite_bottom_depth and position.imag == self.bottom or position in self.rock:
            return 'R'
        return None

    def fill(self, sand_start=500):
        self.top = dict((x, min(p.imag for p in chain(self.rock, self.sand) if p.real == x))
                        for x in set(p.real for p in chain(self.rock, self.sand)))
        self.bottom = max(c.imag for c in chain(self.rock, self.sand))
        if self.infinite_bottom_depth:
            self.bottom += self.infinite_bottom_depth

        drop_count = 0
        while self.drop_sand(sand_start):
            drop_count += 1
        return drop_count

    def drop_sand(self, position):
        if self.at(position) is not None:
            return False
        top = self.top.get(position.real, self.bottom)
        if position.imag < top:
            position = position.real + (top - 1) * 1j
        while position.imag < self.bottom:
            moved = False
            for move in [0 + 1j, -1 + 1j, 1 + 1j]:
                if self.at(position + move) is None:
                    position += move
                    moved = True
                    break
            if not moved:
                self.sand.add(position)
                top = self.top.get(position.real)
                if top and position.imag < top or top is None:
                    self.top[position.real] = position.imag
                return True
        return False


def decode_path(rock_path):
    edges = (list(map(int, edge_str.split(','))) for edge_str in rock_path.split(' -> '))
    rocky_cells = set()
    for (x1, y1), (x2, y2) in pairwise(edges):
        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))
        rocky_cells.update(x + y * 1j
                           for x in range(x1, x2 + 1)
                           for y in range(y1, y2 + 1))
    return rocky_cells


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    cave = Cave()
    with open(filename) as f:
        for rock_path in f.readlines():
            cave.rock.update(decode_path(rock_path.strip()))

    result1 = cave.fill(500)
    print(f"Part 1: quantity of sand added is {result1}")
    if testing and expected1 is not None:
        assert result1 == expected1

    cave.sand.clear()
    cave.infinite_bottom_depth = 2
    result2 = cave.fill(500)
    print(f"Part 2: quantity of sand added is {result2}")
    if testing and expected2 is not None:
        assert result2 == expected2


if __name__ == '__main__':
    main('test.txt', True, 24, None)
    main('input.txt')
