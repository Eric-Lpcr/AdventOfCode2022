from dataclasses import dataclass
from itertools import pairwise
from math import copysign


@dataclass
class Coordinate:
    x: int = 0
    y: int = 0

    def __sub__(self, other):
        return Coordinate(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f'({self.x},{self.y})'

    def __repr__(self):
        return str(self)


class Knot:
    def __init__(self):
        self.coord = Coordinate()

    def __str__(self):
        return str(self.coord)

    def __repr__(self):
        return str(self)

    def move(self, vector):
        self.coord += vector

    def follow(self, leading_knot):
        rope_vector = leading_knot.coord - self.coord
        if abs(rope_vector.x) > 1 or abs(rope_vector.y) > 1:  # knots not touching
            # any axis distance=2 shall be reduced to 1, keeping sign
            follower_move = Coordinate(int(copysign(min(abs(rope_vector.x), 1), rope_vector.x)),
                                       int(copysign(min(abs(rope_vector.y), 1), rope_vector.y)))
            self.move(follower_move)


class Rope:
    directions = {'U': Coordinate(0, 1),
                  'D': Coordinate(0, -1),
                  'L': Coordinate(-1, 0),
                  'R': Coordinate(1, 0)}

    def __init__(self, knot_count=2):
        self.knots = [Knot() for _ in range(knot_count)]
        self.head = self.knots[0]
        self.tail = self.knots[-1]
        self.tail_history = {self.tail.coord}

    def execute_head_moves(self, moves):
        for move in moves:
            direction_code, distance = move.split()
            for _ in range(int(distance)):
                self.move_head(self.directions[direction_code])

    def move_head(self, direction):
        self.head.move(direction)
        for leader, follower in pairwise(self.knots):
            follower.follow(leader)
        self.tail_history.add(self.tail.coord)

    def tail_visited_count(self):
        return len(self.tail_history)


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        moves = f.read().splitlines()

    rope = Rope(2)
    rope.execute_head_moves(moves)
    result1 = rope.tail_visited_count()
    print(f"Part 1: number of positions visited by rope tail is {result1}")
    if testing and expected1 is not None:
        assert result1 == expected1

    rope = Rope(10)
    rope.execute_head_moves(moves)
    result2 = rope.tail_visited_count()
    print(f"Part 2: number of positions visited by rope tail is {result2}")
    if testing and expected2 is not None:
        assert result2 == expected2


if __name__ == '__main__':
    main('test.txt', True, 13, 1)
    main('test2.txt', True, None, 36)
    main('input.txt')
