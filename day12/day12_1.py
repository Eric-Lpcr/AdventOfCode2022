from typing import Iterator

from functools import partial
from implementation import a_star_search, WeightedGraph, GridLocation


class HeightGrid(WeightedGraph):
    def __init__(self, list_of_list):
        self.data = list_of_list
        self.size_x = len(list_of_list[0])
        self.size_y = len(list_of_list)

    def height(self, location: GridLocation):
        x, y = location
        return self.data[y][x]

    def in_bounds(self, location: GridLocation) -> bool:
        (x, y) = location
        return 0 <= x < self.size_x and 0 <= y < self.size_y

    def passable(self, from_location: GridLocation, to_location: GridLocation) -> bool:
        return ord(self.height(to_location)) <= ord(self.height(from_location)) + 1

    def neighbors(self, location: GridLocation) -> Iterator[GridLocation]:
        (x, y) = location
        neighbors = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]  # E W N S
        results = filter(self.in_bounds, neighbors)
        results = filter(partial(self.passable, location), results)
        return results

    def cost(self, from_location: GridLocation, to_location: GridLocation):
        return 1


def find_goals(height_grid):
    start = 0, 0
    end = 0, 0
    for y, line in enumerate(height_grid.data):
        if 'S' in line:
            x = line.index('S')
            start = x, y
            line[x] = 'a'
        if 'E' in line:
            x = line.index('E')
            end = x, y
            line[x] = 'z'
    return start, end


def shortest_path(grid, start, goal):
    came_from, cost_so_far = a_star_search(grid, start, goal)
    return cost_so_far[goal]


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        height_grid = HeightGrid([list(line) for line in f.read().splitlines()])
    start, end = find_goals(height_grid)

    result1 = shortest_path(height_grid, start, end)
    print(f"Part 1: shortest path length is {result1}")
    if testing and expected1 is not None:
        assert result1 == expected1

    result2 = 0
    print(f"Part 2: {result2}")
    if testing and expected2 is not None:
        assert result2 == expected2


if __name__ == '__main__':
    main('test.txt', True, 31, None)
    main('input.txt')
