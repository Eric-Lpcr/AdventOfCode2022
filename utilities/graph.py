# Refactored from: https://www.redblobgames.com/pathfinding/a-star/introduction.html
# Additions from http://formations.telecom-bretagne.eu/pyrat/?p=864

# Sample code from https://www.redblobgames.com/pathfinding/a-star/
# Copyright 2014 Red Blob Games <redblobgames@gmail.com>
#
# Feel free to use this code in your own projects, including commercial projects
# License: Apache v2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>

from __future__ import annotations
from typing import Protocol, Dict, List, Set, Tuple, TypeVar, Optional
import collections
import heapq


T = TypeVar('T')


class PriorityQueue:
    def __init__(self):
        self.heap: List[Tuple[float, T]] = []

    def __bool__(self) -> bool:
        return bool(self.heap)

    def push(self, item: T, priority: float):
        heapq.heappush(self.heap, (priority, item))

    def pop(self) -> T:
        return heapq.heappop(self.heap)[1]


Node = TypeVar('Node')


class Graph(Protocol):

    @property
    def nodes(self) -> Set[Node]:
        return set()

    def neighbors(self, node: Node) -> Set[Node]:
        return set()

    def depth_first_traversal(self, from_node: Node, visitor):
        stack = [from_node]
        visited = set()
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                visitor(current)
                for neighbor in self.neighbors(current):
                    if neighbor not in visited:
                        stack.append(neighbor)

    def breadth_first_traversal(self, from_node: Node, visitor):
        queue = collections.deque()
        visited = {from_node}
        visitor(from_node)
        queue.append(from_node)
        while queue:
            current = queue.pop()
            for neighbor in self.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    visitor(neighbor)
                    queue.append(neighbor)

    def breadth_first_search(self, start: Node, goal: Node):
        queue = collections.deque()
        queue.append(start)
        came_from: Dict[Node, Optional[Node]] = {start: None}
        while queue:
            current: Node = queue.pop()
            if current == goal:
                break
            for next_node in self.neighbors(current):
                if next_node not in came_from:
                    queue.append(next_node)
                    came_from[next_node] = current
        return came_from

    @classmethod
    def reconstruct_path(cls, came_from: Dict[Node, Node], start: Node, goal: Node) -> List[Node]:
        current: Node = goal
        path: List[Node] = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path


def print_visitor(node):
    print(node)


class WeightedGraph(Graph):
    def cost(self, from_node: Node, to_node: Node) -> float: pass

    def dijkstra_search(self, start: Node, goal: Node):
        pqueue = PriorityQueue()
        pqueue.push(start, 0)
        came_from: Dict[Node, Optional[Node]] = {start: None}
        cost_so_far: Dict[Node, float] = {start: 0}

        while pqueue:
            current: Node = pqueue.pop()
            if current == goal:
                break

            for next_node in self.neighbors(current):
                new_cost = cost_so_far[current] + self.cost(current, next_node)
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost
                    pqueue.push(next_node, priority)
                    came_from[next_node] = current

        return came_from, cost_so_far

    def a_star_search(self, start: Node, goal: Node, heuristic=None):
        pqueue = PriorityQueue()
        pqueue.push(start, 0)
        came_from: Dict[Node, Optional[Node]] = {start: None}
        cost_so_far: Dict[Node, float] = {start: 0}

        while pqueue:
            current: Node = pqueue.pop()
            if current == goal:
                break

            for next_node in self.neighbors(current):
                new_cost = cost_so_far[current] + self.cost(current, next_node)
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost
                    if heuristic:
                        priority += heuristic(next_node, goal)
                    pqueue.push(next_node, priority)
                    came_from[next_node] = current

        return came_from, cost_so_far

    def floyd_warshall(self):
        # Distances is the result of the algorithm
        # It is initialized with infinite values where we do not have information
        # The diagonal is initialized to 0, and the graph edges to their values
        nodes = list(self.nodes)
        node_index = {node: i for i, node in enumerate(nodes)}
        size = len(nodes)
        _distances = [[float("inf") for _ in range(size)] for _ in range(size)]
        _predecessors = [[None for _ in range(size)] for _ in range(size)]
        for i, node in enumerate(nodes):
            _distances[i][i] = 0
            for neighbor in self.neighbors(node):
                j = node_index[neighbor]
                _distances[i][j] = self.cost(node, neighbor)
                _predecessors[i][j] = i

        # For every new node to include in the paths
        for k in range(size):
            # For every pair of nodes
            for i in range(size):
                for j in range(size):
                    # We check if it is shorter to go through the new node at some point in the paths
                    # When it is the case, we update the distance
                    potential_new_distance = _distances[i][k] + _distances[k][j]
                    if potential_new_distance < _distances[i][j]:
                        _distances[i][j] = potential_new_distance
                        _predecessors[i][j] = _predecessors[k][j]

        # We return the filled matrix of distances and predecessors
        distances = dict()
        predecessors = dict()
        for i, from_node in enumerate(nodes):
            distances[from_node] = dict()
            predecessors[from_node] = dict()
            for j, to_node in enumerate(nodes):
                distances[from_node][to_node] = _distances[i][j]
                k = _predecessors[i][j]
                predecessors[from_node][to_node] = nodes[k] if k is not None else None

        return distances, predecessors


class SimpleGraph(Graph):
    def __init__(self, directed=True):
        self.edges: Dict[Node, Set[Node]] = collections.defaultdict(set)
        self.directed = directed

    @property
    def nodes(self):
        return self.edges.keys()

    def add_edge(self, node1, node2):
        if node1 not in self.edges:
            self.edges[node1] = set()
        self.edges[node1].add(node2)
        if not self.directed:
            if node2 not in self.edges:
                self.edges[node2] = set()
            self.edges[node2].add(node1)

    def neighbors(self, node: Node) -> Set[Node]:
        return self.edges.get(node, set())


class SimpleWeightedGraph(WeightedGraph):
    def __init__(self, directed=True):
        self.edges: Dict[Node, Dict[Node, float]] = collections.defaultdict(lambda: collections.defaultdict(float))
        self.directed = directed

    @property
    def nodes(self):
        return self.edges.keys()

    def add_edge(self, node1, node2, weight):
        self.edges[node1][node2] = weight
        if not self.directed:
            self.edges[node2][node1] = weight

    def neighbors(self, node: Node) -> Set[Node]:
        return set(self.edges[node].keys())

    def cost(self, from_node: Node, to_node: Node) -> float:
        return self.edges[from_node][to_node]


GridLocation = Tuple[int, int]


class SquareGrid(Graph):
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.walls: List[GridLocation] = []
    
    def in_bounds(self, location: GridLocation) -> bool:
        (x, y) = location
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, location: GridLocation) -> bool:
        return location not in self.walls

    def neighbors(self, location: GridLocation, neighborhood=None) -> Set[GridLocation]:
        (x, y) = location
        if neighborhood is None:
            neighborhood = [(1, 0), (-1, 0), (0, -1), (0, 1)]  # E W N S
            if (x + y) % 2 == 0:  # see "Ugly paths" section for an explanation:
                neighborhood.reverse()  # S N W E
        neighbors = [(x+dx, y+dy) for dx, dy in neighborhood]
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return set(results)


def distance_heuristic(a: GridLocation, b: GridLocation) -> float:
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


class GridWithWeights(SquareGrid, WeightedGraph):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.weights: Dict[GridLocation, float] = {}
    
    def cost(self, from_location: GridLocation, to_location: GridLocation) -> float:
        return self.weights.get(to_location, 1)

    def a_star_search(self, start: GridLocation, goal: GridLocation, heuristic=distance_heuristic):
        return super().a_star_search(start, goal, heuristic)
