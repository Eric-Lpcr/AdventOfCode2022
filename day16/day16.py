from collections import namedtuple
from operator import itemgetter

from itertools import combinations

from dataclasses import dataclass

from utilities.graph import SimpleWeightedGraph


@dataclass
class Valve:
    name: str
    rate: int

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name


def find_optimum_valve_opening(cave, time_limit=30, valve_opening_time=1):
    # compute all shortest paths between any pair of valves
    distances, paths = cave.floyd_warshall()

    most_pressure = float("-inf")
    best_path = None
    all_paths = []

    # backtracking / travelling salesman problem
    # try all permutations of valves, stop a path when time limit is reached
    def open_more_valves(remaining_valves, current_valve, current_path, current_pressure, elapsed_time):
        nonlocal most_pressure, best_path, all_paths, time_limit, valve_opening_time

        all_paths.append((current_path, current_pressure))

        if current_pressure > most_pressure:
            most_pressure = current_pressure
            best_path = current_path
        if elapsed_time >= time_limit:
            return
        for next_valve in remaining_valves:
            next_path = current_path + [next_valve]
            next_elapsed_time = elapsed_time + distances[current_valve][next_valve] + valve_opening_time
            next_pressure = current_pressure + next_valve.rate * (time_limit - next_elapsed_time)
            other_valves = [x for x in remaining_valves if x != next_valve]
            open_more_valves(other_valves, next_valve, next_path, next_pressure, next_elapsed_time)

    valves = [valve for valve in cave.nodes if valve.rate > 0 and valve.name != 'AA']
    start_valve = next(valve for valve in cave.nodes if valve.name == 'AA')
    open_more_valves(valves, start_valve, [start_valve], current_pressure=0, elapsed_time=0)

    return most_pressure, best_path, all_paths


def find_optimum_valve_opening_with_elephant_help(cave, time_limit=26, valve_opening_time=1):
    _, _, all_paths = find_optimum_valve_opening(cave, time_limit, valve_opening_time)

    most_pressure = float("-inf")
    my_best_path = None
    elephant_best_path = None

    bit = 1
    for valve in cave.nodes:
        valve.bit = bit
        bit <<= 1

    def encode_path(path):
        code = 0
        for a_valve in path:
            code |= a_valve.bit
        return code

    all_paths = [(path, pressure, encode_path(path[1:])) for path, pressure in all_paths]
    all_paths.sort(key=itemgetter(1), reverse=True)

    for i, ((my_path, my_pressure, p1), (elephant_path, elephant_pressure, p2)) in enumerate(combinations(all_paths, 2)):
        if my_pressure + elephant_pressure > most_pressure and p1 & p2 == 0:
            most_pressure = my_pressure + elephant_pressure
            my_best_path = my_path
            elephant_best_path = elephant_path
        if my_pressure < most_pressure / 2:
            break
    # print(f'Iteration count: {i}')

    return most_pressure, my_best_path, elephant_best_path


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    cave = SimpleWeightedGraph()
    translation = str.maketrans(',;=', '   ')
    with open(filename) as f:
        valve_infos = dict()
        ValveInfo = namedtuple('ValveInfo', 'valve, neighbor_names')
        for line in f.readlines():
            _, name, _, _, _, rate, _, _, _, _, neighbors = line.translate(translation).split(maxsplit=10)
            valve_infos[name] = ValveInfo(Valve(name, int(rate)), neighbors.split())
        for valve_info in valve_infos.values():
            for neighbor_name in valve_info.neighbor_names:
                cave.add_edge(valve_info.valve, valve_infos[neighbor_name].valve, 1)

    result1, _, _ = find_optimum_valve_opening(cave, time_limit=30)
    print(f"Part 1: most pressure is {result1}")
    if testing and expected1 is not None:
        assert result1 == expected1

    result2, _, _ = find_optimum_valve_opening_with_elephant_help(cave, time_limit=26)
    print(f"Part 2: with elephant, most pressure is {result2}")
    if testing and expected2 is not None:
        assert result2 == expected2


if __name__ == '__main__':
    main('test.txt', True, 1651, 1707)
    main('input.txt')
