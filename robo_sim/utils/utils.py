import math

from .types import Position


def manhattan_distance(a: Position, b: Position) -> float:
    return abs(a.x - b.x) + abs(a.y - b.y)


def euclidean_distance(a: Position, b: Position) -> float:
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)
