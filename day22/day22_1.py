import re

from utilities.coordinates import Coordinate2

Right, Down, Left, Up = 0, 1, 2, 3
Directions = [Coordinate2(1, 0), Coordinate2(0, 1), Coordinate2(-1, 0), Coordinate2(0, -1)]


class Board:
    def __init__(self, cells):
        self.cells = cells
        self.height = len(self.cells)
        self.width = max(len(row) for row in self.cells)

    def in_bounds(self, position: Coordinate2) -> bool:
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height

    def at(self, position: Coordinate2):
        x, y = position
        if 0 <= y < self.height and 0 <= x < len(self.cells[y]):
            return self.cells[y][x]
        else:
            return ' '

    def neighbor_position(self, position, direction):
        neighbor_position = position + direction
        neighbor_position.x %= self.width
        neighbor_position.y %= self.height
        while self.at(neighbor_position) == ' ':
            neighbor_position += direction
            neighbor_position.x %= self.width
            neighbor_position.y %= self.height
        return neighbor_position


def do_moves(moves, start_position, start_orientation, board):
    position = start_position
    orientation = start_orientation
    for move in moves:
        if move == 'R':
            orientation = (orientation + 1) % len(Directions)
        elif move == 'L':
            orientation = (orientation - 1) % len(Directions)
        else:
            steps = int(move)
            for _ in range(steps):
                next_position = board.neighbor_position(position, Directions[orientation])
                if board.at(next_position) == '#':
                    break
                position = next_position
    return position, orientation


def solve_problem(filename, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        board_lines = f.read().splitlines()
        moves_line = board_lines.pop()
        board_lines.pop()
        moves = re.split(r'(\d+)', moves_line)[1:-1]

    board = Board(board_lines)
    start_position = Coordinate2(board.cells[0].index('.'), 0)
    position, orientation = do_moves(moves, start_position, Right, board)

    result1 = (position.y + 1) * 1000 + (position.x + 1) * 4 + orientation
    print(f"Part 1: final password is {result1}")
    if expected1 is not None:
        assert result1 == expected1

    result2 = 0
    print(f"Part 2: {result2}")
    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 6032)
    solve_problem('input.txt', 164014)


if __name__ == '__main__':
    main()
