"""Evaluation functions"""

import math
import typing

import definition

COORDINATES: list[tuple[int, int, int]] = [
    (-1, -1, -1), (-1, -1, 0), (-1, -1, 1),
    (-1, 0, -1), (-1, 0, 0), (-1, 0, 1),
    (-1, 1, -1), (-1, 1, 0), (-1, 1, 1),
    (0, -1, -1), (0, -1, 0), (0, -1, 1),
    (0, 0, -1), (0, 0, 0), (0, 0, 1),
    (0, 1, -1), (0, 1, 0), (0, 1, 1),
    (1, -1, -1), (1, -1, 0), (1, -1, 1),
    (1, 0, -1), (1, 0, 0), (1, 0, 1),
    (1, 1, -1), (1, 1, 0), (1, 1, 1)
]

COST: float = 8 + 4 * math.sqrt(2)
"""average cost"""


exponent = 2
"""exponent of Minkowski distance"""


h: typing.Callable[[list[int]], float] = None
"""heuristic function"""


def chebyshev(data: list[int], ev: int = 0) -> float:
    """Chebyshev distance"""
    for i, v in enumerate(data):
        ev += max((
            abs(COORDINATES[i][j] - COORDINATES[v][j]) for j in range(3)))
    return ev


def euclidean(data: list[int], ev: int = 0) -> float:
    """Euclidean distance"""
    for i, v in enumerate(data):
        ev += math.hypot(
            *(COORDINATES[i][j] - COORDINATES[v][j] for j in range(3)))
    return ev


def manhattan(data: list[int], ev: int = 0) -> float:
    """Manhattan distance"""
    for i, v in enumerate(data):
        for j in range(3):
            ev += abs(COORDINATES[i][j] - COORDINATES[v][j])
    return ev


def hamming(data: list[int], ev: int = 0) -> int:
    """Hamming distance"""
    for i, v in enumerate(data):
        ev += i != v
    return ev


def minkowski(data: list[int], ev: int = 0, *, p: float = 1/exponent) -> float:
    """Minkowski distance"""
    for i, v in enumerate(data):
        for j in range(3):
            ev += abs(COORDINATES[i][j] - COORDINATES[v][j])**p
    return ev**(1/p)


def custom(data: list[int], ev: int = 0) -> int:
    """Custom heuristic function"""
    for i, v in enumerate(data):
        if i in definition.SIDES:
            ev += math.hypot(
                *(COORDINATES[i][j] - COORDINATES[v][j] for j in range(3)))
        elif i in definition.CORNERS:
            for j in range(3):
                ev += abs(COORDINATES[i][j] - COORDINATES[v][j])
    return ev


def g(ev: int, op: definition.OPS) -> float:
    """cost function"""
    if op in ('LR', 'UD', 'FB'):
        return ev + COST / 2
    return ev + COST


def f(ev: int, op: definition.Ways, data: list[int], depth: int, *, algo: definition.Algos) -> float:
    """evaluate function"""
    match algo:
        case 'BFS': return 0
        case 'DFS': return depth - 1
        case 'UCS': return g(ev, op)
        case 'AS': return g(ev, op) + h(data)
        case 'HC': return h(data)
        case _: raise ValueError(algo)
