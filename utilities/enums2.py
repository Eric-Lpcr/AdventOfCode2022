from enum import IntEnum


class IntEnumWithProperty(IntEnum):
    def __new__(cls, *args, **kwargs):
        obj = int.__new__(cls, args[0])
        obj._value_ = args[0]
        return obj

    def __init__(self, _, property_):
        self._property_ = property_
