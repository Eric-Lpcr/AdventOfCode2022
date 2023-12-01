import math

import numpy as np

from utilities.collections2 import Queue, PriorityQueue, Stack
from utilities.timing import timeit


class Blizzards:
    def __init__(self, blizzards):
        self.no_blizzard_cells = list()
        self.period = 0
        self._locate_open_cells(blizzards)

    def _locate_open_cells(self, blizzards):
        winds = np.array([list(b) for b in blizzards])
        north_winds = winds == 'v'
        south_winds = winds == '^'
        east_winds = winds == '<'
        west_winds = winds == '>'

        def expand_and_roll(w, axis, shift):
            period = w.shape[axis]
            w = np.expand_dims(w, axis=0)  # add time dimension
            w = w.repeat(period, axis=0)
            for t in range(1, w.shape[0]):
                w[t] = np.roll(w[t - 1], shift, axis)
            return w

        north_winds = expand_and_roll(north_winds, axis=0, shift=1)  # x axis
        south_winds = expand_and_roll(south_winds, axis=0, shift=-1)
        east_winds = expand_and_roll(east_winds, axis=1, shift=-1)  # y axis
        west_winds = expand_and_roll(west_winds, axis=1, shift=1)

        north_south_period = north_winds.shape[0]  # time axis
        east_west_period = east_winds.shape[0]
        self.period = math.lcm(north_south_period, east_west_period)

        self.no_blizzard_cells.clear()
        for time in range(self.period):
            ns_time = time % north_south_period
            ew_time = time % east_west_period
            any_winds = north_winds[ns_time] | east_winds[ew_time] | south_winds[ns_time] | west_winds[ew_time]
            self.no_blizzard_cells.append([complex(x, y) for y, x in zip(*np.where(~any_winds))])

    def configuration_at_time(self, time):
        return time % self.period

    def open_cells_at_time(self, time):
        return self.no_blizzard_cells[self.configuration_at_time(time)]


@timeit()
def find_path_bfs(blizzards, start_position, exit_position, start_time=0):
    moves = [1 + 0j, 0 + 1j, -1 + 0j, 0 - 1j, 0 + 0j]  # last one means staying in place
    visited_configurations = set()
    positions_to_explore = Queue()
    positions_to_explore.put((start_position, start_time))
    came_from = {(start_position, start_time): None}
    elapsed = None

    while positions_to_explore:
        current_position, minute = current_state = positions_to_explore.get()
        if current_position == exit_position:
            elapsed = minute - start_time
            break

        next_minute = minute + 1
        next_configuration = blizzards.configuration_at_time(next_minute)
        open_cells = blizzards.open_cells_at_time(next_minute)
        for next_position in (current_position + move for move in moves):
            next_state = (next_position, next_minute)
            if ((next_position == start_position or next_position == exit_position or next_position in open_cells)
                    and next_state not in came_from
                    and (next_position, next_configuration) not in visited_configurations):
                positions_to_explore.put(next_state)
                came_from[next_state] = current_state

        visited_configurations.add((current_position, blizzards.configuration_at_time(minute)))

    return elapsed


@timeit()
def find_path_dfs(blizzards, start_position, exit_position, start_time=0):
    moves = [1 + 0j, 0 + 1j, -1 + 0j, 0 - 1j, 0 + 0j]  # last one means staying in place
    visited_states = set()
    visited_configurations = set()
    positions_to_explore = Stack()
    positions_to_explore.put((start_position, start_time))
    best_time = 1e30

    while positions_to_explore:
        current_position, minute = current_state = positions_to_explore.get()
        if current_state not in visited_states:

            if current_position == exit_position and minute < best_time:
                best_time = minute
            next_minute = minute + 1
            if next_minute > best_time:
                continue

            visited_states.add(current_state)
            visited_configurations.add((current_position, blizzards.configuration_at_time(minute)))

            next_configuration = blizzards.configuration_at_time(next_minute)
            open_cells = blizzards.open_cells_at_time(next_minute)
            for next_position in (current_position + move for move in moves):
                next_state = (next_position, next_minute)
                if ((next_position == start_position or next_position == exit_position or next_position in open_cells)
                        and next_state not in visited_states
                        and (next_position, next_configuration) not in visited_configurations):
                    positions_to_explore.put(next_state)

    elapsed = best_time - start_time
    return elapsed


def heuristic(position, goal):
    delta = goal - position
    return abs(delta.real) + abs(delta.imag)


def complex_to_tuple(c: complex):
    return c.real, c.imag  # because PriorityQueue needs element ordering relation


@timeit()
def find_path_astar(blizzards, start_position, exit_position, start_time=0):
    moves = [1 + 0j, 0 + 1j, -1 + 0j, 0 - 1j, 0 + 0j]  # last one means staying in place
    visited_configurations = set()
    positions_to_explore = PriorityQueue()
    positions_to_explore.put((complex_to_tuple(start_position), start_time), 0)
    came_from = {(start_position, start_time): None}
    cost_so_far = {start_position: start_time}
    elapsed = None

    while positions_to_explore:
        current_position, minute = current_state = positions_to_explore.get()
        current_position = complex(*current_position)
        if current_position == exit_position:
            elapsed = minute - start_time
            break

        next_minute = minute + 1
        next_configuration = blizzards.configuration_at_time(next_minute)
        open_cells = blizzards.open_cells_at_time(next_minute)
        for next_position in (current_position + move for move in moves):
            if (next_position == start_position or next_position == exit_position or next_position in open_cells) \
                    and (next_position, next_configuration) not in visited_configurations:
                next_state = (next_position, next_minute)
                if next_state not in cost_so_far or next_minute < cost_so_far[next_state]:
                    cost_so_far[next_state] = next_minute
                    positions_to_explore.put((complex_to_tuple(next_position), next_minute),
                                             next_minute + heuristic(next_position, exit_position))
                    came_from[next_state] = current_state

        visited_configurations.add((current_position, blizzards.configuration_at_time(minute)))

    return elapsed


def solve_problem(filename, expected1=None, expected2=None, find_path=find_path_bfs):
    print(f'--------- {filename}')

    with open(filename) as f:
        blizzards = f.read().splitlines()
        start_position = blizzards[0].index('.') - 1 - 1j
        exit_position = blizzards[-1].index('.') - 1 + (len(blizzards) - 2) * 1j
        blizzards = Blizzards([line.strip('#') for line in blizzards[1:-1]])

    result1 = find_path(blizzards, start_position, exit_position)
    print(f"Part 1: Reaching exit takes {result1} minutes")
    if expected1 is not None:
        assert result1 == expected1

    back_time = find_path(blizzards, exit_position, start_position, result1)
    print(f'   Going back to start took {back_time} minutes')
    reach_again = find_path(blizzards, start_position, exit_position, result1 + back_time)
    print(f'   Reaching exit again took {reach_again} minutes')
    result2 = result1 + back_time + reach_again
    print(f"Part 2: Three way travel takes {result2} minutes")
    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 18, 54, find_path_astar)
    # solve_problem('input.txt', 228, 723, find_path_bfs)
    # solve_problem('input.txt', 228, 723, find_path_dfs)  # Implementation doesn't work...
    solve_problem('input.txt', 228, 723, find_path_astar)


if __name__ == '__main__':
    main()
