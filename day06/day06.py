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


def find_marker_position(datastream, marker_length):
    for pos, marker in enumerate(sliding_window(datastream, marker_length)):
        if len(set(marker)) == marker_length:
            return pos + marker_length
    return None


def solve_problem(filename, expected1=None, expected2=None, testing=False):
    print(f'--------- {filename}')

    if testing:
        datastream = filename
    else:
        with open(filename) as f:
            datastream = f.read().strip()

    result1 = find_marker_position(datastream, marker_length=4)
    print(f"Part 1: start of packet detected at {result1}")
    if expected1 is not None:
        assert result1 == expected1

    result2 = find_marker_position(datastream, marker_length=14)
    print(f"Part 2: start of message detected at {result2}")
    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 7, 19, testing=True)
    solve_problem('bvwbjplbgvbhsrlpgdmjqwftvncz', 5, 23, testing=True)
    solve_problem('nppdvjthqldpwncqszvftbrmjlhg', 6, 23, testing=True)
    solve_problem('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 10, 29, testing=True)
    solve_problem('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 11, 26, testing=True)
    solve_problem('input.txt', 1896, 3452)


if __name__ == '__main__':
    main()
