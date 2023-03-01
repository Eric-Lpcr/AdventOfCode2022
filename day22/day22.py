from collections import defaultdict
from itertools import combinations
from enum import IntEnum
import re

from utilities.enums2 import IntEnumWithProperty
from utilities.collections2 import Queue
from utilities.coordinates import Coordinate2
from utilities.itertools_recipes import first


class Orientation(IntEnumWithProperty):
    Right = 0, Coordinate2(1, 0)
    Down = 1, Coordinate2(0, 1)
    Left = 2, Coordinate2(-1, 0)
    Up = 3, Coordinate2(0, -1)

    @property
    def vector(self) -> Coordinate2:
        return self._property_

    @property
    def at_right(self) -> 'Orientation':
        return self.__class__((self + 1) % len(self.__class__))

    @property
    def at_left(self) -> 'Orientation':
        return self.__class__((self - 1) % len(self.__class__))

    @property
    def at_back(self) -> 'Orientation':
        return self.__class__((self + 2) % len(self.__class__))


class Board:
    WALL = '#'
    OPEN = '.'
    VOID = ' '
    TURN_RIGHT = 'R'
    TURN_LEFT = 'L'

    def __init__(self, cells):
        self.cells = cells
        self.height = len(self.cells)
        self.width = max(len(row) for row in self.cells)

    def at(self, position: Coordinate2) -> str:
        x, y = position
        if 0 <= y < self.height and 0 <= x < len(self.cells[y]):
            return self.cells[y][x]
        else:
            return self.VOID

    def move(self, orders, start_position: Coordinate2, start_orientation: Orientation) -> [Coordinate2, Orientation]:
        position = start_position
        orientation = start_orientation
        for order in orders:
            if order == self.TURN_RIGHT:
                orientation = orientation.at_right
            elif order == self.TURN_LEFT:
                orientation = orientation.at_left
            else:
                steps = int(order)
                for _ in range(steps):
                    next_position, next_orientation = self.step(position, orientation)
                    if self.at(next_position) == self.WALL:
                        break
                    position = next_position
                    orientation = next_orientation
        return position, orientation

    def step(self, position: Coordinate2, orientation: Orientation) -> [Coordinate2, Orientation]:
        move = orientation.vector
        neighbor_position = position + move
        neighbor_position.x %= self.width
        neighbor_position.y %= self.height
        while self.at(neighbor_position) == ' ':
            neighbor_position += move
            neighbor_position.x %= self.width
            neighbor_position.y %= self.height
        return neighbor_position, orientation


class Corner(IntEnumWithProperty):
    TopLeft = 0, Coordinate2(0, 0)
    TopRight = 1, Coordinate2(1, 0)
    BottomRight = 2, Coordinate2(1, 1)
    BottomLeft = 3, Coordinate2(0, 1)

    @property
    def position(self) -> Coordinate2:
        return self._property_


class Side(IntEnum):
    Right = Orientation.Right.value  # to allow correct conversion from or to Orientation
    Bottom = Orientation.Down.value
    Left = Orientation.Left.value
    Top = Orientation.Up.value

    @property
    def vertical(self) -> bool:
        return self in (self.__class__.Left, self.__class__.Right)

    @property
    def horizontal(self) -> bool:
        return not self.vertical


class _CubeGeometry:
    faces = {  # face number (die) => set of corners
        1: set('ABCD'),
        2: set('DCGH'),
        3: set('CBFG'),
        4: set('ADHE'),
        5: set('BAEF'),
        6: set('EFGH'),
    }

    corners = {  # corner => connected corners
        'A': set('BED'),
        'B': set('ACF'),
        'C': set('BDG'),
        'D': set('ACH'),
        'E': set('AFH'),
        'F': set('BEG'),
        'G': set('CFH'),
        'H': set('DEG'),
    }

    sides = dict()  # side {'A', 'B'} => connected face numbers {1, 5}

    def __init__(self):
        for (face1, corners1), (face2, corners2) in combinations(self.faces.items(), 2):
            common_corners = corners1.intersection(corners2)
            if len(common_corners) == 2:
                self.__class__.sides[frozenset(common_corners)] = {face1, face2}

    @classmethod
    def orthogonal_face(cls, face_number: int, side_name: str) -> int:
        return first(cls.sides[frozenset(side_name)] - {face_number})

    @classmethod
    def orthogonal_corner(cls, corner_name: str, face_number: int) -> str:
        return first(cls.corners[corner_name] - cls.faces[face_number])


CubeGeometry = _CubeGeometry()


class Face:
    def __init__(self, layout_position: Coordinate2, size: int):
        self.layout_position = layout_position
        self.size = size
        self.position_on_board = layout_position * self.size
        self.number = 0
        # Face corners 'A', 'B', ... indexed by Corner enum, ..., on board (i.e TopLeft is at position_on_board)
        self._corners = list()
        self.sides = list()  # sides, indexed by Side and oriented towards right or bottom (increasing coordinates)
        self.neighbors = list()  # neighbor face number indexed by Orientation enum on board

    @property
    def name(self) -> str:
        return ''.join(self._corners)

    @property
    def corners(self) -> list[str]:
        return self._corners

    def set_corners(self, top_left: str, top_right: str, bottom_right: str, bottom_left: str) -> None:
        self._corners = [top_left, top_right, bottom_right, bottom_left]

        self.sides = [''] * len(Side)
        self.sides[Side.Right] = top_right + bottom_right
        self.sides[Side.Bottom] = bottom_left + bottom_right
        self.sides[Side.Left] = top_left + bottom_left
        self.sides[Side.Top] = top_left + top_right

        self.neighbors = [0] * len(Side)
        for side in Side:
            self.neighbors[side] = CubeGeometry.orthogonal_face(self.number, self.side_name(side))

    def side_name(self, side: Side) -> str:
        return self.sides[side]

    def find_side(self, side_name: str) -> [Side, bool]:
        if side_name in self.sides:
            side = Side(self.sides.index(side_name))
            reverse = False
        else:
            reverse_side_name = ''.join(reversed(side_name))
            if reverse_side_name in self.sides:
                side = Side(self.sides.index(reverse_side_name))
                reverse = True
            else:
                raise ValueError('Side not found in face')
        return side, reverse

    def corner_name(self, corner: Corner) -> str:
        return self._corners[corner]

    def find_corner(self, corner_name: str) -> Corner:
        if corner_name not in self._corners:
            raise ValueError('Corner not found in face')
        return Corner(self._corners.index(corner_name))

    def corner_position_on_board(self, corner_name: str) -> Coordinate2:
        position_on_face = self.find_corner(corner_name).position * (self.size - 1)
        position_on_board = self.position_on_board + position_on_face
        return position_on_board

    def exit(self, orientation: Orientation, offset: int) -> [Coordinate2, str, int]:
        if 0 > offset >= self.size:
            raise ValueError('Offset out of face size range')
        side = Side(orientation)  # going Left means leaving by Left side
        exit_side_name = self.side_name(side)
        offset_vector = Coordinate2(offset, 0) if side.horizontal else Coordinate2(0, offset)
        exit_position = self.corner_position_on_board(exit_side_name[0])
        exit_position += offset_vector
        to_face_number = self.neighbors[orientation]
        return exit_position, exit_side_name, to_face_number

    def enter(self, side_name: str, offset: int) -> [Coordinate2, Orientation]:
        if 0 > offset >= self.size:
            raise ValueError('Offset out of face size range')
        entry_side, reverse = self.find_side(side_name)
        if reverse:
            offset = -offset
        offset_vector = Coordinate2(offset, 0) if entry_side.horizontal else Coordinate2(0, offset)
        entry_position = self.corner_position_on_board(side_name[0])
        entry_position += offset_vector
        orientation = Orientation(entry_side).at_back  # if we enter Top side, orientation is Down
        return entry_position, orientation

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} {self.number}-{self.name} {self.position_on_board}"


class CubeBoard(Board):
    def __init__(self, cells):
        super().__init__(cells)
        self.teleports = dict()  # Gives neighbor position/orientation from a position/orientation move
        self.faces = dict()  # face number (die) => face object
        self.fold_as_cube()

    def step(self, position: Coordinate2, orientation: Orientation) -> [Coordinate2, Orientation]:
        return self.teleports.get((position.x, position.y, orientation),  # either from teleports
                                  (position + orientation.vector, orientation))  # or computed

    def fold_as_cube(self) -> None:
        self.compute_faces_geometry()
        self.teleports.clear()
        for face in self.faces.values():
            for orientation in Orientation:
                for offset in range(face.size):
                    exit_position, side_name, to_face_number = face.exit(orientation, offset)
                    to_face = self.faces[to_face_number]
                    entry_position, to_orientation = to_face.enter(side_name, offset)
                    self._add_teleport(exit_position, orientation, entry_position, to_orientation)

    def _add_teleport(self,
                      from_position: Coordinate2, from_orientation: Orientation,
                      to_position: Coordinate2, to_orientation: Orientation) -> None:
        assert self.at(from_position) != self.VOID, 'from_position on invalid cell'
        assert self.at(to_position) != self.VOID, 'to_position on invalid cell'
        x1, y1 = from_position
        assert (x1, y1, from_orientation) not in self.teleports, 'Teleport already registered'
        self.teleports[(x1, y1, from_orientation)] = to_position, to_orientation

    def compute_faces_geometry(self) -> None:
        # Compute face size: a developed cube is always 4x3 or 3x4
        size = self.height // 3
        if size != self.width // 4:
            size = self.height // 4

        # Locate faces on board
        faces_layout = defaultdict(None)
        first_face = None
        for j in range(self.height // size):
            for i in range(self.width // size):
                layout_position = Coordinate2(i, j)
                if self.at(layout_position * size) != self.VOID:
                    face = Face(layout_position, size)
                    faces_layout[layout_position] = face
                    if first_face is None:
                        first_face = face
        first_face.number = 1
        first_face.set_corners(*list('ABCD'))
        self.faces[first_face.number] = first_face

        # Connect faces (BFS exploration)
        faces_to_explore = Queue()
        faces_to_explore.put(first_face)
        while faces_to_explore:
            face = faces_to_explore.get()
            for orientation in Orientation:
                next_face = faces_layout.get(face.layout_position + orientation.vector)
                if next_face and next_face.number == 0:
                    shared_side = face.side_name(Side(orientation))
                    number = CubeGeometry.orthogonal_face(face.number, shared_side)

                    top_right, bottom_right, bottom_left, top_left = '', '', '', ''
                    if orientation is Orientation.Right:
                        top_left = face.corner_name(Corner.TopRight)
                        bottom_left = face.corner_name(Corner.BottomRight)
                        bottom_right = CubeGeometry.orthogonal_corner(bottom_left, face.number)
                        top_right = CubeGeometry.orthogonal_corner(top_left, face.number)
                    elif orientation is Orientation.Down:
                        top_left = face.corner_name(Corner.BottomLeft)
                        top_right = face.corner_name(Corner.BottomRight)
                        bottom_right = CubeGeometry.orthogonal_corner(top_right, face.number)
                        bottom_left = CubeGeometry.orthogonal_corner(top_left, face.number)
                    elif orientation is Orientation.Left:
                        top_right = face.corner_name(Corner.TopLeft)
                        bottom_right = face.corner_name(Corner.BottomLeft)
                        bottom_left = CubeGeometry.orthogonal_corner(bottom_right, face.number)
                        top_left = CubeGeometry.orthogonal_corner(top_right, face.number)

                    next_face.number = number
                    next_face.set_corners(top_left, top_right, bottom_right, bottom_left)
                    self.faces[next_face.number] = next_face
                    faces_to_explore.put(next_face)


def compute_password(position: Coordinate2, orientation: Orientation) -> int:
    return (position.y + 1) * 1000 + (position.x + 1) * 4 + orientation


def solve_problem(filename, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        board_lines = f.read().splitlines()
        orders_line = board_lines.pop()
        board_lines.pop()
        orders = re.split(r'(\d+)', orders_line)[1:-1]

    start_position = Coordinate2(board_lines[0].index('.'), 0)
    start_orientation = Orientation.Right

    board = Board(board_lines)
    position, orientation = board.move(orders, start_position, start_orientation)
    result1 = compute_password(position, orientation)
    print(f"Part 1: final password is {result1}")
    if expected1 is not None:
        assert result1 == expected1

    board2 = CubeBoard(board_lines)
    position, orientation = board2.move(orders, start_position, start_orientation)
    result2 = compute_password(position, orientation)
    print(f"Part 2: cube folded, final password is {result2}")
    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 6032, 5031)
    solve_problem('input.txt', 164014, 47525)


if __name__ == '__main__':
    main()
