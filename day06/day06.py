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

    # Performance test
    n = 500
    st = time.process_time()
    for _ in range(n):
        find_marker_position(datastream, marker_length=14)
    elapsed1 = time.process_time() - st
    st = time.process_time()
    for _ in range(n):
        find_marker_position2(datastream, marker_length=14)
    elapsed2 = time.process_time() - st
    print(f"Set length method took {elapsed1} s / Already seen method took {elapsed2} s")


if __name__ == '__main__':
    main('mjqjpqmgbljsphdztnvjfqwrcgsmlb', True, 7, 19)
    main('bvwbjplbgvbhsrlpgdmjqwftvncz', True, 5, 23)
    main('nppdvjthqldpwncqszvftbrmjlhg', True, 6, 23)
    main('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', True, 10, 29)
    main('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', True, 11, 26)
    main('input.txt')
