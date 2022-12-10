import re


class Range:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    def __contains__(self, item):
        if type(item) is type(self):
            return item.begin in self and item.end in self
        else:
            return self.begin <= item <= self.end


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    input_data = list()
    pattern = re.compile(r'(\d+)-(\d+),(\d+)-(\d+)')
    with open(filename) as f:
        for line in f.readlines():
            match = pattern.match(line)
            i1, j1, i2, j2 = [int(g) for g in match.groups()]
            input_data.append((Range(i1, j1), Range(i2, j2)))

    including_pairs = [True for (r1, r2) in input_data if r1 in r2 or r2 in r1]

    result1 = len(including_pairs)
    print(f"Part 1: Number of fully overlapping assignment pairs is {result1}")
    if testing and expected1 is not None:
        assert result1 == expected1

    result2 = 0
    print(f"Part 2: {result2}")

    if testing and expected2 is not None:
        assert result2 == expected2


if __name__ == '__main__':
    main('test.txt', True, 2, None)
    main('input.txt')
