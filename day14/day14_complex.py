from collections import deque

from itertools import pairwise, chain


class Cave:
    def __init__(self,):
        self.rock = set()
        self.sand = set()
        self.bottom = 0  # max y
        self.infinite_bottom_depth = None

    def at(self, position):
        if position in self.sand:
            return 'S'
        if self.infinite_bottom_depth and position.imag == self.bottom or position in self.rock:
            return 'R'
        return None

    def fill(self, sand_start=500):
        self.bottom = max(c.imag for c in chain(self.rock, self.sand))
        if self.infinite_bottom_depth:
            self.bottom += self.infinite_bottom_depth

        drop_count = 0
        while self.drop_sand(sand_start):
            drop_count += 1
        return drop_count

    def drop_sand(self, position, _back_track=deque()):
        if self.at(position) is not None:
            return False  # filled
        if not len(_back_track):
            _back_track.append(position)
        position = _back_track[-1]
        while position.imag < self.bottom:
            for move in [1j, -1 + 1j, 1 + 1j]:
                next_position = position + move
                if self.at(next_position) is None:
                    position = next_position
                    _back_track.append(position)
                    break
            else:
                self.sand.add(position)
                _back_track.pop()
                return True  # rest
        return False  # flows


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
    main('test.txt', True, 24, 93)
    main('input.txt')
