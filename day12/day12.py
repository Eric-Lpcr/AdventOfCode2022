from typing import List

from functools import partial

from utilities.graph import GridLocation, SquareGrid


class ElevationGrid(SquareGrid):
    def __init__(self, list_of_list):
        super().__init__(len(list_of_list[0]), len(list_of_list))
        self.data = list_of_list

    def elevation(self, location: GridLocation):
        x, y = location
        return self.data[y][x]

    def can_climb(self, from_location: GridLocation, to_location: GridLocation) -> bool:
        return ord(self.elevation(to_location)) - ord(self.elevation(from_location)) <= 1

    def can_descend(self, from_location: GridLocation, to_location: GridLocation) -> bool:
        return ord(self.elevation(to_location)) - ord(self.elevation(from_location)) >= -1

    can_move = can_climb

    def neighbors(self, location: GridLocation, neighborhood=None) -> List[GridLocation]:
        x, y = location
        neighbors = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]  # N E S W
        results = filter(self.in_bounds, neighbors)
        results = filter(partial(self.can_move, location), results)
        return list(results)


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
    came_from, goal = grid.breadth_first_search(start, goal)
    path = grid.reconstruct_path(came_from, start, goal)
    return len(path) - 1 if path else 0


def solve_problem(filename, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        height_grid = ElevationGrid([list(line) for line in f.read().splitlines()])
    start, end = find_goals(height_grid)

    result1 = shortest_path(height_grid, start, end)
    print(f"Part 1: shortest path length is {result1}")
    if expected1 is not None:
        assert result1 == expected1

    height_grid.can_move = height_grid.can_descend
    result2 = shortest_path(height_grid, end, lambda location: height_grid.elevation(location) == 'a')
    print(f"Part 2: shortest path length from any 'a' is {result2}")
    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 31, 29)
    solve_problem('input.txt', 383, 377)


if __name__ == '__main__':
    main()
