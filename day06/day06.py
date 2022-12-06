from collections import deque
from itertools import islice
import time


def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) -> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def find_marker_position(datastream, marker_length):
    for pos, marker in enumerate(sliding_window(datastream, marker_length)):
        if len(set(marker)) == marker_length:
            return pos + marker_length
    return None


# Fast exit (as soon as two identical values are found) could be more efficient
# when most tested values are not all unique
def all_unique(iterable):
    seen = set()
    return not any(item in seen or seen.add(item) for item in iterable)


# For the current case, it remains more than 2 times slower than classic set length comparison.
def find_marker_position2(datastream, marker_length):
    for pos, marker in enumerate(sliding_window(datastream, marker_length)):
        seen = set()
        if not any(item in seen or seen.add(item) for item in marker):
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


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    if testing:
        datastream = filename
    else:
        with open(filename) as f:
            datastream = f.read().strip()

    result1 = find_marker_position(datastream, marker_length=4)
    print(f"Part 1: start of packet detected at {result1}")
    if testing and expected1 is not None:
        assert result1 == expected1

    result2 = find_marker_position(datastream, marker_length=14)
    print(f"Part 2: start of message detected at {result2}")
    if testing and expected2 is not None:
        assert result2 == expected2

    result3 = david_finds_the_marker_position(datastream, marker_length=14)
    print(f"Part 2: David found {result3}")
    if testing and expected2 is not None:
        assert result3 == expected2

    # Performance test
    n = 500
    st = time.process_time()
    for _ in range(n):
        find_marker_position(datastream, marker_length=14)
    elapsed1 = time.process_time() - st
    st = time.process_time()
    print(f"Set length method took {elapsed1} s")
    for _ in range(n):
        find_marker_position2(datastream, marker_length=14)
    elapsed2 = time.process_time() - st
    print(f"Already seen method took {elapsed2} s")
    st = time.process_time()
    for _ in range(n):
        david_finds_the_marker_position(datastream, marker_length=14)
    elapsed3 = time.process_time() - st
    print(f"David Spiller method took {elapsed3} s")
    st = time.process_time()
    for _ in range(n):
        find_marker_position4(datastream, marker_length=14)
    elapsed4 = time.process_time() - st
    print(f"Basic method took {elapsed4} s")


if __name__ == '__main__':
    main('mjqjpqmgbljsphdztnvjfqwrcgsmlb', True, 7, 19)
    main('bvwbjplbgvbhsrlpgdmjqwftvncz', True, 5, 23)
    main('nppdvjthqldpwncqszvftbrmjlhg', True, 6, 23)
    main('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', True, 10, 29)
    main('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', True, 11, 26)
    main('input.txt')
