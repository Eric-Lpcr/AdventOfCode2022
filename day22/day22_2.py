import re

from utilities.coordinates import Coordinate2

Right, Down, Left, Up = 0, 1, 2, 3
Directions = [Coordinate2(1, 0), Coordinate2(0, 1), Coordinate2(-1, 0), Coordinate2(0, -1)]


class Board:
    def __init__(self, cells, cube=False):
        self.cells = cells
        self.height = len(self.cells)
        self.width = max(len(row) for row in self.cells)
        self.neighbors = dict()  # Gives neighbor position/orientation from a position/orientation move
        self.fold_cube() if cube else self.wrap_flat()

    def in_bounds(self, position: Coordinate2) -> bool:
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height

    def at(self, position: Coordinate2):
        x, y = position
        if 0 <= y < self.height and 0 <= x < len(self.cells[y]):
            return self.cells[y][x]
        else:
            return ' '

    def _add_neighbors(self, x1, y1, orientation1, x2, y2, orientation2):
        assert (x1, y1, orientation1) not in self.neighbors, 'Neighbor already registered'
        assert (x2, y2, (orientation2 + 2) % 4) not in self.neighbors, 'Neighbor already registered'
        assert self.at(Coordinate2(x1, y1)) != ' ', 'Neighbor on invalid cell'
        assert self.at(Coordinate2(x2, y2)) != ' ', 'Neighbor on invalid cell'

        self.neighbors[(x1, y1, orientation1)] = Coordinate2(x2, y2), orientation2
        self.neighbors[(x2, y2, (orientation2 + 2) % 4)] = Coordinate2(x1, y1), (orientation1 + 2) % 4  # opposite

    def wrap_flat(self):
        self.neighbors.clear()
        side = self.height // 3
        for i in range(side):
            self._add_neighbors(2*side, i, Left, 3*side-1, i, Left)  # Face 1
            self._add_neighbors(2*side+i, 0, Up, 2*side+i, 3*side-1, Up)  # Face 1 to 5
            self._add_neighbors(i, side, Up, i, 2*side-1, Up)  # Face 2
            self._add_neighbors(side+i, side, Up, side+i, 2*side-1, Up)  # Face 3
            self._add_neighbors(0, side+i, Left, 3*side-1, side+i, Left)  # Face 2 to 4
            self._add_neighbors(2*side, 2*side+i, Left, 4*side-1, 2*side+i, Left)  # Face 5 to 6
            self._add_neighbors(3*side+i, 2*side, Up, 3*side+i, 3*side-1, Up)  # Face 6

    def fold_cube(self):
        self.neighbors.clear()
        side = self.height // 3
        for i in range(side):
            self._add_neighbors(2*side+i, 0, Up, side-1-i, side, Down)  # Face 1 to 2
            self._add_neighbors(2*side, i, Left, side+i, side, Down)  # Face 1 to 3
            self._add_neighbors(3*side-1, i, Right, 4*side-1, 3*side-1-i, Left)  # Face 1 to 6
            self._add_neighbors(i, 2*side-1, Down, 3*side-1-i, 3*side-1, Up)  # Face 2 to 5
            self._add_neighbors(0, side+i, Right, 4*side-1-i, 3*side-1, Up)  # Face 2 to 6
            self._add_neighbors(side+i, 2*side-1, Down, 2*side, 3*side-1-i, Right)  # Face 3 to 5
            self._add_neighbors(3*side-1, side+i, Right, 4*side-1-i, 2*side, Down)  # Face 4 to 6

    def neighbor_position(self, position, orientation):
        return self.neighbors.get((position.x, position.y, orientation),  # either from folding
                                  (position + Directions[orientation], orientation))  # or computed


def do_moves(moves, start_position, start_orientation, board):
    position = start_position
    orientation = start_orientation
    for move in moves:
        # print(move)
        if move == 'R':
            orientation = (orientation + 1) % len(Directions)
        elif move == 'L':
            orientation = (orientation - 1) % len(Directions)
        else:
            steps = int(move)
            for _ in range(steps):
                next_position, next_orientation = board.neighbor_position(position, orientation)
                if board.at(next_position) == '#':
                    break
                position = next_position
                orientation = next_orientation
                # print(position)
    return position, orientation


def solve_problem(filename, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        board_lines = f.read().splitlines()
        moves_line = board_lines.pop()
        board_lines.pop()
        moves = re.split(r'(\d+)', moves_line)[1:-1]

    try:
        board = Board(board_lines)
    except AssertionError:
        print("That doesn't work anymore!")
        return

    start_position = Coordinate2(board.cells[0].index('.'), 0)

    position, orientation = do_moves(moves, start_position, Right, board)
    result1 = (position.y + 1) * 1000 + (position.x + 1) * 4 + orientation
    print(f"Part 1: final password is {result1}")

    board.fold_cube()
    position, orientation = do_moves(moves, start_position, Right, board)
    result2 = (position.y + 1) * 1000 + (position.x + 1) * 4 + orientation
    print(f"Part 2: cube folded, final password is {result2}")
    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 6032)
    solve_problem('input.txt', 164014)


if __name__ == '__main__':
    main()
