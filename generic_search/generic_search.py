from __future__ import annotations
import heapq
from collections import deque
from typing import (TypeVar, Iterable, Sequence, Generic, Optional,
                    List, Callable, Set, Deque, Dict, Any)
from typing_extensions import Protocol


T = TypeVar('T')


def linear_contains(iterable: Iterable[T], key: T) -> bool:
    for item in iterable:
        if item == key:
            return True
    return False


C = TypeVar('C', bound='Comparable')


class Comparable(Protocol):
    def __eq__(self, other: Any) -> bool:
        ...

    def __lt__(self: C, other: C) -> bool:
        ...

    def __gt__(self: C, other: C) -> bool:
        return (not self < other) and self != other

    def __le__(self: C, other: C) -> bool:
        return self < other or self == other

    def __ge__(self: C, other: C) -> bool:
        return not self < other


def binary_contains(sequence: Sequence[C], key: C) -> bool:
    low = 0
    high = len(sequence) - 1
    while low <= high:
        mid = (low + high) // 2
        if sequence[mid] == key:
            return True
        elif sequence[mid] > key:
            high = mid - 1
        elif sequence[mid] < key:
            low = mid + 1

    return False


class Stack(Generic[T]):

    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()

    def __repr__(self) -> str:
        return repr(self._container)


class Queue(Generic[T]):
    def __init__(self) -> None:
        self._container: Deque[T] = deque()

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.popleft()

    def __repr__(self) -> str:
        return repr(self._container)


class PriorityQueue(Generic[T]):

    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        heapq.heappush(self._container, item)

    def pop(self) -> T:
        return heapq.heappop(self._container)

    def __repr__(self) -> str:
        return repr(self._container)


class Node(Generic[T]):
    def __init__(
            self,
            state: T,
            parent: Optional[Node],
            cost: float = 0.0,
            heuristic: float = 0.0,
    ) -> None:
        self.state: T = state
        self.parent: Optional[Node] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic

    def __lt__(self, other: Node) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def dfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]) -> Optional[Node[T]]:
    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(initial, None))

    explored: Set[T] = {initial}

    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state

        if goal_test(current_state):
            return current_node

        for child in successors(current_state):
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))

    return None


def bfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]) -> Optional[Node[T]]:
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))
    explored: Set[T] = {initial}

    while not frontier.empty:
        current_node = frontier.pop()
        current_state = current_node.state

        if goal_test(current_state):
            return current_node

        for child in successors(current_state):
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))

    return None


def astar(
        initial: T,
        goal_test: Callable[[T], bool],
        successors: Callable[[T], List[T]],
        heuristic: Callable[[T], float]
) -> Optional[Node[T]]:
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0.0, heuristic(initial)))

    explored: Dict[T, float] = {initial: 0.0}

    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: Node[T] = current_node.state

        if goal_test(current_state):
            return current_node

        for child in successors(current_state):
            new_cost: float = current_node.cost + 1

            if new_cost not in explored or explored[new_cost] > new_cost:
                explored[child] = new_cost
                frontier.push(Node(child, current_node, new_cost, heuristic(child)))

    return None


def node_to_path(node: Node[T]) -> List[T]:
    path: List[T] = [node.state]

    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path


