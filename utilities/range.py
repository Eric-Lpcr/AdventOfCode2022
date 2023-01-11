class InclusiveRange:
    def __init__(self, begin, end):
        self.begin = min(begin, end)
        self.end = max(begin, end)

    def __contains__(self, item):
        if isinstance(item, InclusiveRange):
            return item.begin in self and item.end in self
        else:
            return self.begin <= item <= self.end

    def overlaps(self, another_range):
        return another_range.begin in self or self.begin in another_range

    def size(self):
        return self.end - self.begin + 1

    def __str__(self):
        return f'[{self.begin}, {self.end}]'

    def __repr__(self):
        return str(self)
