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


def solve_problem(filename, expected1=None, expected2=None, testing=False):
    print(f'--------- {filename}')

    if testing:
        datastream = filename
    else:
        with open(filename) as f:
            datastream = f.read().strip()

    result1 = find_marker(datastream, marker_length=4)
    print(f"Part 1: packet starts at {result1}")
    if expected1 is not None:
        assert result1 == expected1

    result2 = 0
    print(f"Part 2: {result2}")

    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 7, testing=True)
    solve_problem('bvwbjplbgvbhsrlpgdmjqwftvncz', 5, testing=True)
    solve_problem('nppdvjthqldpwncqszvftbrmjlhg', 6, testing=True)
    solve_problem('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 10, testing=True)
    solve_problem('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 11, testing=True)
    solve_problem('input.txt', 1896)


if __name__ == '__main__':
    main()
