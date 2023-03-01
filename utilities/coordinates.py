import numbers

from math import prod

from operator import sub, add, eq

from typing import Iterable


class Coordinate(Iterable):

    @property
    def dimension(self):
        return 0

    def __iter__(self): pass

    def manhattan_to(self, other):
        return (self - other).manhattan()

    def manhattan(self):
        return sum(map(abs, self))

    def __eq__(self, other):
        return all(map(eq, self, other))

    def __add__(self, other):
        return type(self)(*map(add, self, other))

    def __sub__(self, other):
        return type(self)(*map(sub, self, other))

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return type(self)(*map(lambda x: x * other, self))
        else:
            raise TypeError(f'Unsupported parameter type {type(other)}')

    def __hash__(self):
        return hash(tuple(self))

    def __str__(self):
        return '[' + ','.join(str(c) for c in self) + ']'

    def __repr__(self):
        return str(self)


class Box:
    def __init__(self, lower: Coordinate, upper: Coordinate = None):
        self.lower = lower
        self.upper = upper if upper is not None else lower

    def dimension(self):
        return self.lower.dimension

    def __contains__(self, coord: Coordinate):
        return all(low <= c <= up for low, c, up in zip(self.lower, coord, self.upper))

    def extend(self, coord: Coordinate):
        if coord not in self:
            self.lower = type(self.lower)(*map(min, self.lower, coord))
            self.upper = type(self.upper)(*map(max, self.upper, coord))

    @property
    def size(self):
        return self.upper - self.lower

    @property
    def grid_size(self):
        return self.size + self.lower.__class__.ones()

    @property
    def volume(self):
        return prod(self.size)

    @property
    def grid_volume(self):
        return prod(self.grid_size)


class Coordinate2(Coordinate):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def dimension(self):
        return 2

    @classmethod
    def zeroes(cls):
        return cls(0, 0)

    @classmethod
    def ones(cls):
        return cls(1, 1)

    def __iter__(self):
        yield self.x
        yield self.y


class Coordinate3(Coordinate):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @property
    def dimension(self):
        return 3

    @classmethod
    def zeroes(cls):
        return cls(0, 0, 0)

    @classmethod
    def ones(cls):
        return cls(1, 1, 1)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z
