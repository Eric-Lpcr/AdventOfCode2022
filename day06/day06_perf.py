from collections import deque

from day06 import find_marker_position, sliding_window
from utilities.timing import timeit


@timeit(rounds=500, verbose=False)
def measure_function(f, *args, **kwargs):
    f(*args, **kwargs)


def all_unique(iterable):
    # Fast exit (as soon as two identical values are found) could be more efficient
    # when most tested values are not all unique
    seen = set()
    return not any(item in seen or seen.add(item) for item in iterable)


# For the current case, it remains more than 2 times slower than classic set length comparison.
def find_marker_position2(datastream, marker_length):
    for pos, marker in enumerate(sliding_window(datastream, marker_length)):
        if all_unique(marker):
            return pos + marker_length
    return None


# Adapted from David Spiller: https://github.com/dspi/ZTM_AdventOfCode2022/blob/main/day06/tuning_trouble.py
def david_finds_the_marker_position(datastream, marker_length):
    marker = []
    for pos, char in enumerate(datastream):  # reading one by one and never sub indexing for marker length
        if char in marker:
            del marker[:marker.index(char)+1]  # reduce marker till duplicate character, included
        marker.append(char)
        if len(marker) == marker_length:
            return pos + 1


# A neat solution with a maxed size deque, a bit faster than sliding_window generic iteration tool
def find_marker_position4(datastream, marker_length):
    marker = deque(maxlen=marker_length)
    for pos, char in enumerate(datastream):
        marker.append(char)
        if len(set(marker)) == marker_length:
            return pos + marker_length


def solve_problem(filename):
    print(f'--------- {filename}')

    with open(filename) as f:
        datastream = f.read().strip()

    print(f"Set length method:")
    measure_function(find_marker_position, datastream, marker_length=14)

    print(f"Already seen method:")
    measure_function(find_marker_position2, datastream, marker_length=14)

    print(f"David Spiller method:")
    measure_function(david_finds_the_marker_position, datastream, marker_length=14)

    print(f"Basic method:")
    measure_function(find_marker_position4, datastream, marker_length=14)


def main():
    solve_problem('input.txt')


if __name__ == '__main__':
    main()
