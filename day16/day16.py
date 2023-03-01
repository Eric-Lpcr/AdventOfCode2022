from math import comb

from collections import namedtuple, defaultdict
from operator import itemgetter, xor

from itertools import combinations

from dataclasses import dataclass

from utilities.graph import SimpleWeightedGraph
from utilities.timing import timeit


@dataclass
class Valve:
    name: str
    rate: int

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f'{self.name}({self.rate})'


def reduce_cave_graph(cave, start_valve):
    valves_to_remove = set()
    for valve, neighbors in cave.edges.items():
        if valve.rate == 0 and valve != start_valve:
            for (v1, d1), (v2, d2) in combinations(neighbors.items(), 2):
                cave.add_edge(v1, v2, d1+d2)
                cave.add_edge(v2, v1, d1 + d2)
                del cave.edges[v1][valve], cave.edges[v2][valve]
            valves_to_remove.add(valve)
    for valve in valves_to_remove:
        del cave.edges[valve]


@timeit(verbose=True)
def find_optimum_valve_opening(cave, start_valve, time_limit=30, valve_opening_time=1):
    # compute all shortest paths between any pair of valves
    distances, paths = cave.floyd_warshall()
    minimum_travel_time = min(min(filter(lambda x: x > 0, d.values())) for d in distances.values())

    most_pressure = float("-inf")
    best_path = None
    all_paths = []

    # backtracking / travelling salesman problem
    # try all permutations of valves, stop a path when time limit is reached
    def open_more_valves(remaining_valves, current_valve, current_path, current_pressure, elapsed_time):
        nonlocal most_pressure, best_path, all_paths, time_limit, valve_opening_time

        if current_pressure > most_pressure:
            most_pressure = current_pressure
            best_path = current_path
        all_paths.append((current_path, current_pressure))

        if elapsed_time >= time_limit - minimum_travel_time - valve_opening_time:
            return  # travelling + opening another valve would be useless

        for next_valve in remaining_valves:
            next_path = current_path + [next_valve]
            next_elapsed_time = elapsed_time + distances[current_valve][next_valve] + valve_opening_time
            next_pressure = current_pressure + next_valve.rate * (time_limit - next_elapsed_time)
            other_valves = [x for x in remaining_valves if x != next_valve]
            open_more_valves(other_valves, next_valve, next_path, next_pressure, next_elapsed_time)

    valves = [valve for valve in cave.nodes if valve.rate > 0 and valve.name != 'AA']
    open_more_valves(valves, start_valve, [start_valve], current_pressure=0, elapsed_time=0)

    return most_pressure, best_path, all_paths


@timeit(verbose=True)
def find_optimum_valve_opening_with_elephant_help(cave, start_valve, time_limit=26, valve_opening_time=1):
    _, _, all_paths = find_optimum_valve_opening(cave, start_valve, time_limit, valve_opening_time)

    most_pressure = float("-inf")
    my_best_path = None
    elephant_best_path = None

    bit = 1
    for valve in cave.nodes:
        valve.bit = bit
        bit <<= 1

    def encode_path(p):
        code = 0
        for a_valve in p:
            code |= a_valve.bit
        return code

    # compact all_paths to retain the max pressure and path for all paths involving the same valves (same encoding)
    all_paths_dict = defaultdict(lambda: ([], -1))
    for path, pressure in all_paths:
        encoded_path = encode_path(path[1:])  # Don't encode start value as it will be common
        if pressure > all_paths_dict[encoded_path][1]:
            all_paths_dict[encoded_path] = (path, pressure)
    all_paths = [(encoded_path, path, pressure) for encoded_path, (path, pressure) in all_paths_dict.items()]

    # sort all paths according to pressure, get the max first to be able to stop iteration later
    all_paths.sort(key=itemgetter(2), reverse=True)

    all_valves_path_encoding = encode_path([valve for valve in cave.nodes if valve != start_valve])

    iteration_count = cutoff_count = 0
    for i, (p1, my_path, my_pressure) in enumerate(all_paths[:-1]):
        if my_pressure < most_pressure / 2:
            break  # can't improve result, as the elephant contribution will be less, because of ordering
        p2 = xor(p1, all_valves_path_encoding)  # test with complementary path key
        if p2 in all_paths_dict:
            iteration_count += 1
            cutoff_count += 1
            elephant_path, elephant_pressure = all_paths_dict[p2]
            if my_pressure + elephant_pressure > most_pressure:
                most_pressure = my_pressure + elephant_pressure
                my_best_path = my_path
                elephant_best_path = elephant_path
        else:
            for (p2, elephant_path, elephant_pressure) in all_paths[i+1:]:
                if my_pressure + elephant_pressure <= most_pressure:
                    break  # can't improve result, as the elephant contribution will decrease, because of ordering
                iteration_count += 1
                if p1 & p2 == 0:
                    most_pressure = my_pressure + elephant_pressure
                    my_best_path = my_path
                    elephant_best_path = elephant_path

    print(f'    iteration count: {iteration_count} over comb({len(all_paths)}, 2) = {comb(len(all_paths), 2)}')
    print(f'    cutoff count: {cutoff_count}')

    return most_pressure, my_best_path, elephant_best_path


def solve_problem(filename, expected1=None, expected2=None):
    print(f'--------- {filename}')

    cave = SimpleWeightedGraph()
    translation = str.maketrans(',;=', '   ')
    with open(filename) as f:
        valve_data = dict()
        ValveInfo = namedtuple('ValveInfo', 'valve, neighbor_names')
        for line in f.readlines():
            _, name, _, _, _, rate, _, _, _, _, neighbors = line.translate(translation).split(maxsplit=10)
            valve_data[name] = ValveInfo(Valve(name, int(rate)), neighbors.split())
        for valve_info in valve_data.values():
            for neighbor_name in valve_info.neighbor_names:
                cave.add_edge(valve_info.valve, valve_data[neighbor_name].valve, 1)

    start_valve = next(valve for valve in cave.nodes if valve.name == 'AA')

    reduce_cave_graph(cave, start_valve)
    print(f'Cave problem reduced from {len(valve_data)} to {len(cave.nodes)} valves')

    result1, _, _ = find_optimum_valve_opening(cave, start_valve, time_limit=30)
    print(f"Part 1: most pressure is {result1}")
    if expected1 is not None:
        assert result1 == expected1

    result2, _, _ = find_optimum_valve_opening_with_elephant_help(cave, start_valve, time_limit=26)
    print(f"Part 2: with elephant, most pressure is {result2}")
    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 1651, 1707)
    solve_problem('input.txt', 1737, 2216)


if __name__ == '__main__':
    main()
