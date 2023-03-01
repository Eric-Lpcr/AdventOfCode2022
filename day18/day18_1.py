from itertools import combinations


def manhattan(cube1, cube2):
    return sum(abs(c2 - c1) for c1, c2 in zip(cube1, cube2))


def solve_problem(filename, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        cubes = dict((tuple(map(int, line.split(','))), 6) for line in f.readlines())

    for cube1, cube2 in combinations(cubes.keys(), 2):
        if manhattan(cube1, cube2) == 1:
            cubes[cube1] -= 1
            cubes[cube2] -= 1

    result1 = sum(cubes.values())
    print(f"Part 1: lava droplet surface area is {result1}")
    if expected1 is not None:
        assert result1 == expected1

    result2 = 0
    print(f"Part 2: {result2}")
    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 64)
    solve_problem('input.txt', 4314)


if __name__ == '__main__':
    main()
