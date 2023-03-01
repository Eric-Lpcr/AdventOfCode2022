from math import copysign

from dataclasses import dataclass


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


class Rope:
    directions = {'U': Coordinate(0, 1),
                  'D': Coordinate(0, -1),
                  'L': Coordinate(-1, 0),
                  'R': Coordinate(1, 0)}

    def __init__(self):
        self.head = Coordinate()
        self.tail = Coordinate()
        self.tail_history = {self.tail}

    def execute_head_moves(self, moves):
        for move in moves:
            direction, distance = move.split()
            for _ in range(int(distance)):
                self.move_head(self.directions[direction])

    def move_head(self, move):
        self.head += move
        rope_vector = self.head - self.tail
        if abs(rope_vector.x) > 1 or abs(rope_vector.y) > 1:  # knots not touching
            # any axis distance=2 shall be reduced to 1, keeping sign
            tail_move = Coordinate(int(copysign(min(abs(rope_vector.x), 1), rope_vector.x)),
                                   int(copysign(min(abs(rope_vector.y), 1), rope_vector.y)))
            self.tail += tail_move
            self.tail_history.add(self.tail)

    def tail_visited_count(self):
        return len(self.tail_history)


def solve_problem(filename, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        moves = f.read().splitlines()

    rope = Rope()
    rope.execute_head_moves(moves)
    result1 = rope.tail_visited_count()
    print(f"Part 1: number of positions visited by rope tail is {result1}")
    if expected1 is not None:
        assert result1 == expected1

    result2 = 0
    print(f"Part 2: {result2}")
    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 13)
    solve_problem('input.txt', 6037)


if __name__ == '__main__':
    main()
