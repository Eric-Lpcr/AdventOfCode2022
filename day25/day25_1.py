from functools import lru_cache

from typing import Union, List

from itertools import zip_longest

from operator import itemgetter


@lru_cache
def power_of_5(power):
    return 5 ** power


class Snafu:
    def __init__(self, value: Union[int, str, List] = 0):
        self.digits = []
        self._str = ''
        if isinstance(value, str):
            self.digits = [-2 if c == '=' else -1 if c == '-' else int(c) for c in value]
        elif isinstance(value, int):
            self.digits = [value]
        elif isinstance(value, list):
            self.digits = value
        else:
            raise TypeError('Unexpected input')

    def __int__(self):
        return sum(digit * power_of_5(power) for power, digit in enumerate(reversed(self.digits)))

    def __add__(self, other):
        if not isinstance(other, Snafu):
            other = Snafu(other)
        return Snafu(list(reversed([d + other_d for d, other_d in self._zip(other)])))

    def _zip(self, other):
        return zip_longest(reversed(self.digits), reversed(other.digits), fillvalue=0)

    def __eq__(self, other):
        if isinstance(other, Snafu):
            return all(d == other_d for d, other_d in self._zip(other))
        elif isinstance(other, int):
            return int(self) == other
        elif isinstance(other, str):
            return str(self) == other
        else:
            return self == other

    def _normalize(self):
        def reduce(digit):
            e = digit // 5
            digit -= e * 5
            if digit > 2:
                digit -= 5
                e += 1
            return digit, e

        self.digits.reverse()
        i = 0
        while i < len(self.digits):
            self.digits[i], extra = reduce(self.digits[i])
            if extra != 0:
                if i == len(self.digits) - 1:
                    self.digits.append(extra)
                else:
                    self.digits[i + 1] += extra
            i += 1
        self.digits.reverse()

    def __str__(self):
        self._normalize()
        return ''.join(['=-012'[d+2] for d in self.digits])

    def __repr__(self):
        return f'Snafu({self})'


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        if testing:
            f.readline()  # column names
            data = [(snafu, int(decimal)) for snafu, decimal in map(str.split, f.readlines())]
            snafus = [Snafu(snafu) for snafu in map(itemgetter(0), data)]
        else:
            snafus = [Snafu(line.strip()) for line in f.readlines()]

    if testing:
        print(f"Testing")
        for snafu, decimal in data:
            computed_decimal = int(Snafu(snafu))
            computed_snafu = str(Snafu(decimal))
            print(f"decimal(s'{snafu}') = {computed_decimal}, snafu({decimal}) = s'{computed_snafu}'")
            assert computed_decimal == decimal, \
                f'Problem converting {snafu} to decimal, got {computed_decimal}, expecting {decimal}'
            assert computed_snafu == snafu, \
                f'Problem converting {decimal} to snafu, got {computed_snafu}, expecting {snafu}'
        print()

    result1 = sum(snafus, Snafu(0))
    print(f"Part 1: sum is {result1} (decimal {int(result1)})")
    if testing and expected1 is not None:
        assert result1 == expected1

    result2 = None
    print(f"Part 2: result is offered by young elf")
    if testing and expected2 is not None:
        assert result2 == expected2


if __name__ == '__main__':
    main('notice.txt', True, None, None)
    main('test.txt', True, '2=-1=0', None)
    main('input.txt')
