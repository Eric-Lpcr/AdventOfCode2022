from collections import namedtuple

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

    # backtracking / travelling salesman problem
    # try all permutations of valves, stop a path when time limit is reached
    def open_more_valves(remaining_valves, current_valve, current_path, current_pressure, elapsed_time):
        nonlocal most_pressure, best_path, time_limit, valve_opening_time
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

    return most_pressure, best_path


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

    result1, _ = find_optimum_valve_opening(cave)
    print(f"Part 1: most pressure is {result1}")
    if testing and expected1 is not None:
        assert result1 == expected1

    result2 = 0
    print(f"Part 2: {result2}")
    if testing and expected2 is not None:
        assert result2 == expected2


if __name__ == '__main__':
    main('test.txt', True, 1651, 1707)
    main('input.txt')
