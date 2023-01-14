import operator

import functools
from typing import Union, List
from itertools import zip_longest


@functools.total_ordering
class BaseDecimal:
    Base = None
    Offset = 0
    Symbols = ''
    Prefix = ''
    Suffix = ''

    def __init__(self, value=0):
        """value can be a string representation with symbols, an integer,
        another BaseDecimal, or a list of integer digits"""
        self._digits = []
        if isinstance(value, str):
            value = value.lstrip(self.Prefix).rstrip(self.Suffix)
            self._digits = [self.Symbols.index(c) + self.Offset for c in reversed(value)]
        elif isinstance(value, list):
            self._digits = list(reversed(value))
            self.normalize()
        elif isinstance(value, int):
            self._digits = [value]
            self.normalize()
        elif isinstance(value, type(self)):
            self._digits = list(value._digits)
        elif isinstance(value, BaseDecimal):
            self._digits = [int(value)]
            self.normalize()
        else:
            raise TypeError('Unexpected input')

    @property
    def digits(self):
        return list(reversed(self._digits))

    def __int__(self):
        return sum(digit * self.__power(self.Base, position) for position, digit in enumerate(self._digits))

    @staticmethod
    @functools.lru_cache
    def __power(base, exp):
        return pow(base, exp)

    def __add__(self, other):
        res = type(self)()
        if isinstance(other, int):
            res._digits = list(self._digits)
            res._digits[0] += other
        else:
            if not isinstance(other, type(self)):
                other = type(self)(other)
            res._digits = [d + other_d for d, other_d in self._zip_with(other)]
        res.normalize()
        return res

    def __neg__(self):
        return type(self)(list(map(operator.neg, self.digits)))

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        return type(self)(int(self) * int(other))

    def __truediv__(self, other) -> float:
        return int(self) / int(other)

    def __floordiv__(self, other):
        return type(self)(int(self) // int(other))

    def __mod__(self, other):
        return type(self)(int(self) % int(other))

    def _zip_with(self, other):
        return zip_longest(self._digits, reversed(other.digits), fillvalue=0)

    def __eq__(self, other):
        self.normalize()
        if isinstance(other, type(self)):
            other.normalize()
            return all(d == other_d for d, other_d in self._zip_with(other))
        elif isinstance(other, int):
            return int(self) == other
        elif isinstance(other, str):
            return str(self) == other
        else:
            return self == other

    def __lt__(self, other):
        return int(self) < int(other)

    def normalize(self):
        i = 0
        max_digit = self.Base - 1 + self.Offset
        while i < len(self._digits):
            digit = self._digits[i]
            if digit < self.Offset or digit > max_digit:
                extra = digit // self.Base
                digit -= extra * self.Base
                if digit > max_digit:
                    digit -= self.Base
                    extra += 1
                self._digits[i] = digit
                if extra != 0:
                    if i + 1 == len(self._digits):
                        self._digits.append(extra)
                    else:
                        self._digits[i + 1] += extra
            i += 1

    def __str__(self):
        self.normalize()
        return self.Prefix + \
            ''.join(self.Symbols[digit - self.Offset] for digit in reversed(self._digits)) + \
            self.Suffix

    def __repr__(self):
        return f'{self.__class__.__name__}({self})'
