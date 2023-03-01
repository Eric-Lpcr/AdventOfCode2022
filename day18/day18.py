from collections import deque
from math import prod

from utilities.coordinates import Coordinate3, Box
from utilities.itertools_recipes import first

Neighborhood = [Coordinate3(-1, 0, 0), Coordinate3(1, 0, 0),
                Coordinate3(0, -1, 0), Coordinate3(0, 1, 0),
                Coordinate3(0, 0, -1), Coordinate3(0, 0, 1)]


def neighbors(coord):
    return [coord + offset for offset in Neighborhood]


def surface_area(lava_droplet):
    surface = 0
    for cube in lava_droplet:
        surface += sum(neighbor not in lava_droplet for neighbor in neighbors(cube))
    return surface


def external_surface_area(lava_droplet):
    # compute a bounding box
    bounds = Box(first(lava_droplet))
    for cube in lava_droplet:
        bounds.extend(cube)

    # add margins
    bounds.extend(bounds.lower - Coordinate3(1, 1, 1))
    bounds.extend(bounds.upper + Coordinate3(1, 1, 1))

    # and flood fill it with a breadth first traversal
    # each time we encounter a lava cube, add a face to the lava droplet surface
    surface = 0
    frontier = deque()
    frontier.append(bounds.lower)
    visited = {bounds.lower}
    while frontier:
        cube = frontier.pop()
        for next_cube in neighbors(cube):
            if next_cube not in bounds or next_cube in visited:
                continue
            if next_cube in lava_droplet:
                surface += 1
                # don't add this lava cube to visited because it can have a neighbor on another face
                # don't add it to frontier because we don't want to explore it
            else:
                frontier.append(next_cube)
                visited.add(next_cube)

    volume = prod(d + 1 for d in bounds.upper - bounds.lower) - len(visited)

    return surface, volume


def solve_problem(filename, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        lava_droplet = set(Coordinate3(*map(int, line.split(','))) for line in f.readlines())

    result1 = surface_area(lava_droplet)
    print(f"Part 1: lava droplet surface area is {result1}")
    if expected1 is not None:
        assert result1 == expected1

    result2, volume = external_surface_area(lava_droplet)
    print(f"Part 2: lava droplet external surface area is {result2}")
    if expected2 is not None:
        assert result2 == expected2
    print(f"        [lava droplet external volume is {volume}]")


def main():
    solve_problem('test.txt', 64, 58)
    solve_problem('input.txt', 4314, 2444)


if __name__ == '__main__':
    main()
