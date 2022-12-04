import re


class InclusiveRange:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    def __contains__(self, item):
        if isinstance(item, InclusiveRange):
            return item.begin in self and item.end in self
        else:
            return self.begin <= item <= self.end

    def overlap(self, another_range):
        return self in another_range or another_range.begin in self or another_range.end in self

    def __str__(self):
        return f'[{self.begin}, {self.end}]'

    def __repr__(self):
        return str(self)


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    input_data = list()
    pattern = re.compile(r'(\d+)-(\d+),(\d+)-(\d+)')
    with open(filename) as f:
        for line in f.readlines():
            match = pattern.match(line)
            i1, j1, i2, j2 = [int(g) for g in match.groups()]
            input_data.append((InclusiveRange(i1, j1), InclusiveRange(i2, j2)))

    fully_overlapping_pairs = (r1 in r2 or r2 in r1 for (r1, r2) in input_data)  # True/False generator

    result1 = sum(fully_overlapping_pairs)  # sum of booleans gives number of True (1), can't use len on generator
    print(f"Part 1: number of fully overlapping assignment pairs is {result1}")
    if testing and expected1 is not None:
        assert result1 == expected1

    overlapping_pairs = (r1.overlap(r2) for (r1, r2) in input_data)
    # overlapping_pairs = map(InclusiveRange.overlap, *zip(*input_data))  # star abuse!

    result2 = sum(overlapping_pairs)
    print(f"Part 2: number of overlapping assignment pairs is {result2}")

    if testing and expected2 is not None:
        assert result2 == expected2


if __name__ == '__main__':
    main('test.txt', True, 2, 4)
    main('input.txt')
