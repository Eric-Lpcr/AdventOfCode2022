from itertools import count

import math
import operator
import re
from dataclasses import dataclass
from math import ceil

from utilities.collections2 import Stack
from utilities.itertools_recipes import take


@dataclass
class Resources:
    ore: float = 0
    clay: float = 0
    obsidian: float = 0
    geode: float = 0

    def __add__(self, other):
        # return Resources(*list(x + y for x, y in zip(self, other)))
        return Resources(
            self.ore + other.ore,
            self.clay + other.clay,
            self.obsidian + other.obsidian,
            self.geode + other.geode
        )

    def __sub__(self, other):
        # return Resources(*list(x - y for x, y in zip(self, other)))
        return Resources(
            self.ore - other.ore,
            self.clay - other.clay,
            self.obsidian - other.obsidian,
            self.geode - other.geode
        )

    def __mul__(self, other):
        if isinstance(other, Resources):
            # return Resources(*list(x * y for x, y in zip(self, other)))
            return Resources(
                self.ore * other.ore,
                self.clay * other.clay,
                self.obsidian * other.obsidian,
                self.geode * other.geode
            )
        else:
            # return Resources(*list(x * other for x in self))
            return Resources(
                self.ore * other,
                self.clay * other,
                self.obsidian * other,
                self.geode * other
            )

    def __truediv__(self, other):
        if isinstance(other, Resources):
            # return Resources(*list(math.inf if y == 0 else x / y for x, y in zip(self, other)))
            return Resources(
                math.inf if other.ore == 0 else self.ore / other.ore,
                math.inf if other.clay == 0 else self.clay / other.clay,
                math.inf if other.obsidian == 0 else self.obsidian / other.obsidian,
                math.inf if other.geode == 0 else self.geode / other.geode
            )
        else:
            # return Resources(*list(x / other for x in self))
            return Resources(
                self.ore / other,
                self.clay / other,
                self.obsidian / other,
                self.geode / other
            )

    def __iter__(self):
        yield self.ore
        yield self.clay
        yield self.obsidian
        yield self.geode

    def __hash__(self):
        # return hash(tuple(iter(self)))
        return hash((self.ore, self.clay, self.obsidian, self.geode))

    def __str__(self):
        return f'{self.ore} ore, {self.clay} clay, {self.obsidian} obsidian, {self.geode} geode'


@dataclass
class Blueprint:
    oreRobotCost: Resources
    clayRobotCost: Resources
    obsidianRobotCost: Resources
    geodeRobotCost: Resources

    def __iter__(self):
        yield self.oreRobotCost
        yield self.clayRobotCost
        yield self.obsidianRobotCost
        yield self.geodeRobotCost


@dataclass
class State:
    time_left: int
    robots: Resources
    materials: Resources

    def __str__(self):
        return f'Time left {self.time_left} / Robots: {self.robots} / Materials: {self.materials}'

    def __hash__(self):
        return hash((self.time_left, self.robots, self.materials))


class RobotFactory:
    def __init__(self, blueprint, construction_time=1):
        self.blueprint = blueprint
        self.construction_time = construction_time
        self.productions = [Resources(1, 0, 0, 0),
                            Resources(0, 1, 0, 0),
                            Resources(0, 0, 1, 0),
                            Resources(0, 0, 0, 1)]

    def delay_to_build(self, robot_cost, materials, robots) -> int:
        max_delay = max(delay for delay, cost in zip((robot_cost - materials) / robots, robot_cost) if cost)
        if math.isinf(max_delay):
            return max_delay
        else:
            max_delay = max(0, ceil(max_delay))  # zero delay if resources are available
            return max_delay + self.construction_time

    def get_delays(self, materials, robots):
        delays = Resources(*list(self.delay_to_build(cost, materials, robots) for cost in self.blueprint))
        return reversed(list(zip(delays, self.blueprint, self.productions)))  # reversed puts higher value robots first


def mine_most_geodes(blueprint, initial_state) -> int:
    factory = RobotFactory(blueprint)
    most_geodes = 0

    max_needed_robots = Resources(max(robot_cost.ore for robot_cost in factory.blueprint),
                                  max(robot_cost.clay for robot_cost in factory.blueprint),
                                  max(robot_cost.obsidian for robot_cost in factory.blueprint),
                                  initial_state.time_left)  # no limit for geode robots, one each minute is a max

    states_to_explore = Stack()
    states_to_explore.put(initial_state)
    visited_states = set()
    while states_to_explore:
        current_state = states_to_explore.get()
        geodes_at_end = current_state.materials.geode + current_state.robots.geode * current_state.time_left
        if geodes_at_end > most_geodes:
            most_geodes = geodes_at_end

        for delay, cost, robots_built in factory.get_delays(current_state.materials, current_state.robots):
            if current_state.time_left <= delay:
                continue  # no time left to build this robot
            if any(map(operator.gt, current_state.robots + robots_built, max_needed_robots)):
                continue  # building this robot is useless as max resource needed each minute is already reached
            if geodes_at_end + current_state.time_left * current_state.time_left // 2 <= most_geodes:
                continue  # even if a geode robot could be built each remaining minute, it wouldn't suffice

            next_state = State(current_state.time_left - delay,
                               current_state.robots + robots_built,
                               current_state.materials + current_state.robots * delay - cost)
            if next_state not in visited_states:
                states_to_explore.put(next_state)

        visited_states.add(current_state)

    return most_geodes


def blueprints_most_geodes(blueprints, initial_state):
    result = []
    for index, blueprint in enumerate(blueprints):
        most_geodes = mine_most_geodes(blueprint, initial_state)
        print(f'Blueprint {index + 1} gives at most {most_geodes} geodes')
        result.append(most_geodes)
    return result


def compute_blueprints_quality(blueprints, initial_state):
    most_geodes = blueprints_most_geodes(blueprints, initial_state)
    global_quality = sum(most_geodes * index for most_geodes, index in zip(most_geodes, count(1)))
    return global_quality


def solve_problem(filename, expected1=None, expected2=None):
    print(f'--------- {filename}')

    blueprints = []
    with open(filename) as f:
        pattern = re.compile(r'Blueprint \d+: Each ore robot costs (\d+) ore. '
                             r'Each clay robot costs (\d+) ore. '
                             r'Each obsidian robot costs (\d+) ore and (\d+) clay. '
                             r'Each geode robot costs (\d+) ore and (\d+) obsidian.')
        for line in f:
            match = pattern.match(line)
            blueprints.append(Blueprint(Resources(int(match.group(1))),
                                        Resources(int(match.group(2))),
                                        Resources(int(match.group(3)), int(match.group(4))),
                                        Resources(int(match.group(5)), 0, int(match.group(6)))))

    initial_state = State(time_left=24, robots=Resources(1), materials=Resources())

    result1 = compute_blueprints_quality(blueprints, initial_state)
    print(f"Part 1: blueprints quality level is {result1}")
    if expected1 is not None:
        assert result1 == expected1

    initial_state.time_left = 32
    result2 = math.prod(blueprints_most_geodes(take(3, blueprints), initial_state))
    print(f"Part 2: first three blueprints largest geodes product is {result2}")
    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 33, 56*62)
    solve_problem('input.txt', 1413, 21080)


if __name__ == '__main__':
    main()
