from collections import defaultdict
from itertools import combinations

import re

from utilities.collections2 import Queue
from utilities.coordinates import Coordinate2
from utilities.itertools_recipes import first

Right, Down, Left, Up = 0, 1, 2, 3
Directions = [Coordinate2(1, 0), Coordinate2(0, 1), Coordinate2(-1, 0), Coordinate2(0, -1)]


class Board:
    def __init__(self, cells):
        self.cells = cells
        self.height = len(self.cells)
        self.width = max(len(row) for row in self.cells)

    def at(self, position: Coordinate2):
        x, y = position
        if 0 <= y < self.height and 0 <= x < len(self.cells[y]):
            return self.cells[y][x]
        else:
            return ' '

    def do_moves(self, moves, start_position, start_orientation):
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
                    next_position, next_orientation = self.neighbor_position(position, orientation)
                    if self.at(next_position) == '#':
                        break
                    position = next_position
                    orientation = next_orientation
        return position, orientation

    def neighbor_position(self, position, orientation):
        move = Directions[orientation]
        neighbor_position = position + move
        neighbor_position.x %= self.width
        neighbor_position.y %= self.height
        while self.at(neighbor_position) == ' ':
            neighbor_position += move
            neighbor_position.x %= self.width
            neighbor_position.y %= self.height
        return neighbor_position, orientation


TopLeft, TopRight, BottomRight, BottomLeft = 0, 1, 2, 3
Corner_positions = [Coordinate2(0, 0), Coordinate2(1, 0), Coordinate2(1, 1), Coordinate2(0, 1)]

Top = Up
Bottom = Down

Cube_faces = {  # face number (die), list of corners
    1: set('ABCD'),
    2: set('DCGH'),
    3: set('CBFG'),
    4: set('ADHE'),
    5: set('BAEF'),
    6: set('EFGH'),
}

Cube_corners = {  # corner => connected corners
    'A': set('BED'),
    'B': set('ACF'),
    'C': set('BDG'),
    'D': set('ACH'),
    'E': set('AFH'),
    'F': set('BEG'),
    'G': set('CFH'),
    'H': set('DEG'),
}

Cube_edges = dict()  # edge 'AB' => connected face numbers {1, 5}
for (face1, corners1), (face2, corners2) in combinations(Cube_faces.items(), 2):
    common_corners = corners1.intersection(corners2)
    if len(common_corners) == 2:
        Cube_edges[frozenset(common_corners)] = {face1, face2}


class Face:
    def __init__(self, layout_position, side):
        self.layout_position = layout_position
        self.side = side
        self.grid_position = layout_position * self.side
        self.number = 0
        # Face corners 'A', 'B', ... indexed by TopLeft, TopRight, ..., on grid (i.e TopLeft is at grid_position)
        self.corners = ['Z'] * 4
        self.neighbors = list()  # neighbor face number indexed by orientation on grid

    def get_edges(self):
        """return edges names, oriented on axis (increasing coordinates), indexed by orientation"""
        return [
            self.corners[TopRight] + self.corners[BottomRight],  # Right
            self.corners[BottomLeft] + self.corners[BottomRight],  # Bottom
            self.corners[TopLeft] + self.corners[BottomLeft],  # Left
            self.corners[TopLeft] + self.corners[TopRight],  # Top
        ]

    def get_edge(self, orientation):
        return self.get_edges()[orientation]

    def get_grid_position(self, corner):
        index = self.corners.index(corner)
        face_position = Corner_positions[index] * (self.side - 1)
        grid_position = self.grid_position + face_position
        return grid_position

    def exit(self, orientation, offset):
        if 0 > offset >= self.side:
            raise ValueError('index out of range')
        exit_edge = self.get_edge(orientation)
        offset_vector = Coordinate2(offset, 0) if orientation in (Up, Down) else Coordinate2(0, offset)
        exit_position = self.get_grid_position(exit_edge[0]) + offset_vector
        to_face_number = self.neighbors[orientation]
        return exit_position, exit_edge, to_face_number

    def enter(self, entry_edge, offset):
        if 0 > offset >= self.side:
            raise ValueError('index out of range')
        if entry_edge in self.get_edges():
            entry_side = self.get_edges().index(entry_edge)
            offset_vector = Coordinate2(offset, 0) if entry_side in (Up, Down) else Coordinate2(0, offset)
        else:
            reversed_entry_edge = ''.join(reversed(entry_edge))
            if reversed_entry_edge in self.get_edges():
                entry_side = self.get_edges().index(reversed_entry_edge)
                offset_vector = Coordinate2(-offset, 0) if entry_side in (Up, Down) else Coordinate2(0, -offset)
            else:
                raise ValueError('entry edge not found on this face')

        entry_position = self.get_grid_position(entry_edge[0]) + offset_vector
        orientation = (entry_side + 2) % len(Directions)  # if we enter Top, orientation is Down
        return entry_position, orientation

    def __str__(self):
        return f"{self.number}-{''.join(self.corners)} {self.grid_position}"


class CubeBoard(Board):
    def __init__(self, cells):
        super().__init__(cells)
        self.neighbors = dict()  # Gives neighbor position/orientation from a position/orientation move
        self.faces = dict()  # face number (die) => face object
        self.fold_cube()

    def neighbor_position(self, position, orientation):
        return self.neighbors.get((position.x, position.y, orientation),  # either from folding
                                  (position + Directions[orientation], orientation))  # or computed

    def fold_cube(self):
        self._localise_faces()
        self._compute_faces_neighbors()

        self.neighbors.clear()
        for face in self.faces.values():
            for orientation in range(4):
                for offset in range(face.side):
                    exit_position, exit_edge, to_face_number = face.exit(orientation, offset)
                    to_face = self.faces[to_face_number]
                    entry_position, to_orientation = to_face.enter(exit_edge, offset)
                    self._add_cell_neighbor(exit_position, orientation, entry_position, to_orientation)

    def _add_cell_neighbor(self, from_position, from_orientation, to_position, to_orientation):
        assert self.at(from_position) != ' ', 'from_position on invalid cell'
        assert self.at(to_position) != ' ', 'to_position on invalid cell'
        x1, y1 = from_position
        assert (x1, y1, from_orientation) not in self.neighbors, 'Neighbor already registered'
        self.neighbors[(x1, y1, from_orientation)] = to_position, to_orientation

    def _compute_face_side_size(self):
        side = self.height // 3
        if side != self.width // 4:
            side = self.height // 4
        return side

    def _localise_faces(self):
        side = self._compute_face_side_size()

        faces_layout = defaultdict(None)
        first_face = None
        for j in range(self.height // side):
            for i in range(self.width // side):
                layout_position = Coordinate2(i, j)
                if self.at(layout_position * side) != ' ':
                    face = Face(layout_position, side)
                    faces_layout[layout_position] = face
                    if first_face is None:
                        first_face = face
        first_face.number = 1
        first_face.corners = list('ABCD')
        self.faces[first_face.number] = first_face

        faces_to_explore = Queue()
        faces_to_explore.put(first_face)

        while faces_to_explore:
            face = faces_to_explore.get()
            for orientation, direction in enumerate(Directions):
                next_face = faces_layout.get(face.layout_position + direction)
                if next_face and next_face.number == 0:
                    common_edge = face.get_edge(orientation)
                    next_face.number = first(Cube_edges[frozenset(common_edge)] - {face.number})
                    self.faces[next_face.number] = next_face

                    top_right, bottom_right, bottom_left, top_left = next_face.corners
                    if orientation == Right:
                        top_left = face.corners[TopRight]
                        bottom_left = face.corners[BottomRight]
                        bottom_right = first(Cube_corners[bottom_left] - set(face.corners))
                        top_right = first(Cube_corners[top_left] - set(face.corners))
                    elif orientation == Down:
                        top_left = face.corners[BottomLeft]
                        top_right = face.corners[BottomRight]
                        bottom_right = first(Cube_corners[top_right] - set(face.corners))
                        bottom_left = first(Cube_corners[top_left] - set(face.corners))
                    elif orientation == Left:
                        top_right = face.corners[TopLeft]
                        bottom_right = face.corners[BottomLeft]
                        bottom_left = first(Cube_corners[bottom_right] - set(face.corners))
                        top_left = first(Cube_corners[top_right] - set(face.corners))

                    next_face.corners = [top_left, top_right, bottom_right, bottom_left]
                    faces_to_explore.put(next_face)

    def _compute_faces_neighbors(self):
        for face in self.faces.values():
            for edge in face.get_edges():  # edges are stored according to orientations
                neighbor = first(Cube_edges[frozenset(edge)] - {face.number})
                face.teleports.append(neighbor)  # so are the neighbor faces


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        board_lines = f.read().splitlines()
        moves_line = board_lines.pop()
        board_lines.pop()
        moves = re.split(r'(\d+)', moves_line)[1:-1]
    start_position = Coordinate2(board_lines[0].index('.'), 0)
    start_orientation = Right

    board = Board(board_lines)
    position, orientation = board.do_moves(moves, start_position, start_orientation)
    result1 = (position.y + 1) * 1000 + (position.x + 1) * 4 + orientation
    print(f"Part 1: final password is {result1}")
    if testing and expected1 is not None:
        assert result1 == expected1

    board2 = CubeBoard(board_lines)
    position, orientation = board2.do_moves(moves, start_position, start_orientation)
    result2 = (position.y + 1) * 1000 + (position.x + 1) * 4 + orientation
    print(f"Part 2: cube folded, final password is {result2}")
    if testing and expected2 is not None:
        assert result2 == expected2


if __name__ == '__main__':
    main('test.txt', True, 6032, 5031)
    main('input.txt', True, 164014, 47525)
