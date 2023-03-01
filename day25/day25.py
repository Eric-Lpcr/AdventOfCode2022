from operator import itemgetter

from utilities.base_decimal import BaseDecimal


class Snafu(BaseDecimal):
    Base = 5
    Offset = -2
    Symbols = '=-012'


def solve_problem(filename, expected1=None, expected2=None, testing=False):
    print(f'--------- {filename}')

    with open(filename) as f:
        if testing:
            f.readline()  # column names
            data = [(snafu, int(decimal)) for snafu, decimal in map(str.split, f.readlines())]
            snafus = [Snafu(snafu) for snafu in map(itemgetter(0), data)]
        else:
            snafus = [Snafu(line) for line in f.read().splitlines()]

    if testing:
        print(f"Testing")
        for snafu, decimal in data:
            computed_decimal = int(Snafu(snafu))
            computed_snafu = Snafu(decimal)
            print(f'decimal({snafu}) = {computed_decimal}, snafu({decimal}) = {computed_snafu}')
            assert computed_decimal == decimal, \
                f'Problem converting {snafu} to decimal, got {computed_decimal}, expecting {decimal}'
            assert computed_snafu == snafu, \
                f'Problem converting {decimal} to snafu, got {computed_snafu}, expecting {snafu}'
        print()

    result1 = sum(snafus, Snafu(0))
    print(f"Part 1: sum is {result1} (decimal {int(result1)})")
    if expected1 is not None:
        assert result1 == expected1

    result2 = None
    print(f"Part 2: is offered by young elf")
    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('notice.txt', testing=True)
    solve_problem('test.txt', '2=-1=0', testing=True)
    solve_problem('input.txt', '2=12-100--1012-0=012')


if __name__ == '__main__':
    main()
