from collections import deque
from itertools import islice


def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) -> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def find_marker(datastream, marker_length):
    for pos, marker in enumerate(sliding_window(datastream, marker_length)):
        if len(set(marker)) == marker_length:
            return pos + marker_length
    return -1


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    if testing:
        datastream = filename
    else:
        with open(filename) as f:
            datastream = f.read().strip()

    result1 = find_marker(datastream, marker_length=4)
    print(f"Part 1: packet starts at {result1}")
    if testing and expected1 is not None:
        assert result1 == expected1

    result2 = 0
    print(f"Part 2: {result2}")

    if testing and expected2 is not None:
        assert result2 == expected2


if __name__ == '__main__':
    main('mjqjpqmgbljsphdztnvjfqwrcgsmlb', True, 7, None)
    main('bvwbjplbgvbhsrlpgdmjqwftvncz', True, 5, None)
    main('nppdvjthqldpwncqszvftbrmjlhg', True, 6, None)
    main('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', True, 10, None)
    main('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', True, 11, None)
    main('input.txt')
