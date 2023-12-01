import math
from collections import deque

from utilities.collections2 import Queue


def rotate_right(i, n_bits):
    lsb = i & 1
    return i >> 1 | lsb << (n_bits - 1)


def rotate_left(i, n_bits):
    msb = (i >> (n_bits - 1)) & 1
    return i << 1 | msb


class Blizzards:
    def __init__(self, blizzards):
        self.no_blizzard_cells = list()
        self.period = 0
        self._locate_open_cells(blizzards)

    def _locate_open_cells(self, blizzards):
        north_winds = deque(int(line.translate(str.maketrans('v<^>.', '10000')), 2) for line in blizzards)
        south_winds = deque(int(line.translate(str.maketrans('v<^>.', '00100')), 2) for line in blizzards)
        north_winds_at_time = list()
        south_winds_at_time = list()
        north_south_period = len(blizzards)
        for time in range(north_south_period):
            north_winds_at_time.append(list(north_winds))
            south_winds_at_time.append(list(south_winds))
            north_winds.rotate(1)
            south_winds.rotate(-1)

        east_winds = list(int(line.translate(str.maketrans('v<^>.', '01000')), 2) for line in blizzards)
        west_winds = list(int(line.translate(str.maketrans('v<^>.', '00010')), 2) for line in blizzards)
        east_winds_at_time = list()
        west_winds_at_time = list()
        east_west_period = len(blizzards[0])
        for time in range(east_west_period):
            east_winds_at_time.append(east_winds)
            west_winds_at_time.append(west_winds)
            east_winds = list(rotate_left(e, east_west_period) for e in east_winds)
            west_winds = list(rotate_right(w, east_west_period) for w in west_winds)

        self.no_blizzard_cells.clear()
        self.period = math.lcm(north_south_period, east_west_period)
        x_masks = [1 << x for x in reversed(range(east_west_period))]
        for time in range(self.period):
            ns_time = time % north_south_period
            ew_time = time % east_west_period
            all_winds = [n | e | s | w for n, e, s, w in zip(north_winds_at_time[ns_time],
                                                             east_winds_at_time[ew_time],
                                                             south_winds_at_time[ns_time],
                                                             west_winds_at_time[ew_time])]
            self.no_blizzard_cells.append(list())
            for y, winds in enumerate(all_winds):
                self.no_blizzard_cells[time].extend(complex(x, y) 
                                                    for x, mask in enumerate(x_masks) if not winds & mask)

    def configuration_at_time(self, time):
        return time % self.period

    def open_cells_at_time(self, time):
        return self.no_blizzard_cells[self.configuration_at_time(time)]


def find_path(blizzards, start_position, exit_position):
    moves = [1+0j, 0+1j, -1+0j, 0-1j, 0+0j]  # last one means staying in place
    visited_configurations = set()
    positions_to_explore = Queue()
    positions_to_explore.put((start_position, 0))
    came_from = {(start_position, 0): None}
    steps = None
    while positions_to_explore:
        current_position, minute = positions_to_explore.get()
        if current_position == exit_position:
            steps = minute
            break

        next_minute = minute + 1
        next_configuration = blizzards.configuration_at_time(next_minute)
        open_cells = blizzards.open_cells_at_time(next_minute)
        for move in moves:
            next_position = current_position + move
            if next_position == start_position or next_position == exit_position or next_position in open_cells:
                if (next_position, next_minute) not in came_from \
                        and (next_position, next_configuration) not in visited_configurations:
                    positions_to_explore.put((next_position, next_minute))
                    came_from[(next_position, next_minute)] = (current_position, minute)

        visited_configurations.add((current_position, blizzards.configuration_at_time(minute)))

    return steps


def solve_problem(filename, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        blizzards = f.read().splitlines()
        start_position = blizzards[0].index('.') - 1 - 1j
        exit_position = blizzards[-1].index('.') - 1 + (len(blizzards) - 2) * 1j
        blizzards = Blizzards([line.strip('#') for line in blizzards[1:-1]])

    result1 = find_path(blizzards, start_position, exit_position)
    print(f"Part 1: number of steps to exit is {result1}")
    if expected1 is not None:
        assert result1 == expected1

    result2 = 0
    print(f"Part 2: {result2}")
    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 18)
    solve_problem('input.txt', 228)


if __name__ == '__main__':
    main()
