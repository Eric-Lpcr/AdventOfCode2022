from ast import literal_eval

from functools import total_ordering


class PacketItem:
    @staticmethod
    def build(content):
        if isinstance(content, list):
            return ListPacketItem(content)
        elif isinstance(content, int):
            return IntPacketItem(content)

    def __repr__(self):
        return f'{type(self).__name__} {self}'


@total_ordering
class IntPacketItem(PacketItem):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __lt__(self, other):
        if isinstance(other, IntPacketItem):
            return self.value < other.value
        elif isinstance(other, ListPacketItem):
            return [self] < other.items
        else:
            raise TypeError("'<' not supported between instances of " 
                            f"'{type(self).__name__}' and '{type(other).__name__}'")

    def __eq__(self, other):
        if isinstance(other, IntPacketItem):
            return self.value == other.value
        elif isinstance(other, ListPacketItem):
            return [self] == other.items
        else:
            raise TypeError("'==' not supported between instances of " 
                            f"'{type(self).__name__}' and '{type(other).__name__}'")


@total_ordering
class ListPacketItem(PacketItem):
    def __init__(self, content):
        self.items = [PacketItem.build(item) for item in content]

    def __str__(self):
        return f"[{', '.join(str(item) for item in self.items)}]"

    def __lt__(self, other):
        if isinstance(other, IntPacketItem):
            return self.items < [other]
        elif isinstance(other, ListPacketItem):
            return self.items < other.items
        else:
            raise TypeError("'<' not supported between instances of " 
                            f"'{type(self).__name__}' and '{type(other).__name__}'")

    def __eq__(self, other):
        if isinstance(other, IntPacketItem):
            return self.items == [other]
        elif isinstance(other, ListPacketItem):
            return self.items == other.items
        else:
            raise TypeError("'==' not supported between instances of "
                            f"'{type(self).__name__}' and '{type(other).__name__}'")


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    packet_pairs = list()
    with open(filename) as f:
        for packet_pair_block in f.read().split('\n\n'):
            packet_pair = tuple(PacketItem.build(literal_eval(line)) for line in packet_pair_block.splitlines())
            packet_pairs.append(packet_pair)

    if testing:
        for i, (p1, p2) in enumerate(packet_pairs):
            print(f"Pair {i+1} {'NOT ' if p1 > p2 else ''}in the right order")
            print(p1)
            print(p2)

    result1 = sum(i+1 for i, (p1, p2) in enumerate(packet_pairs) if p1 <= p2)
    print(f"Part 1: sum of right order pair indexes is {result1}")
    if testing and expected1 is not None:
        assert result1 == expected1

    result2 = 0
    print(f"Part 2: {result2}")
    if testing and expected2 is not None:
        assert result2 == expected2


if __name__ == '__main__':
    main('test.txt', True, 13, None)
    main('input.txt')
