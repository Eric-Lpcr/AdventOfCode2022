import heapq

from typing import TypeVar, List, Tuple

import collections


T = TypeVar('T')


class Stack:
    def __init__(self, *args, **kwargs):
        self.elements = collections.deque(*args, **kwargs)

    def __bool__(self) -> bool:
        return bool(self.elements)

    def empty(self) -> bool:
        return not self.elements

    def __len__(self):
        return len(self.elements)

    def __iter__(self):
        return iter(self.elements)

    def put(self, x: T):
        self.elements.append(x)

    def get(self) -> T:
        return self.elements.pop()


class Queue(Stack):
    def get(self) -> T:
        return self.elements.popleft()


class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[float, T]] = []

    def __bool__(self) -> bool:
        return bool(self.elements)

    def empty(self) -> bool:
        return not self.elements

    def __len__(self):
        return len(self.elements)

    def __iter__(self):
        return iter(self.elements)

    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> T:
        return heapq.heappop(self.elements)[1]
