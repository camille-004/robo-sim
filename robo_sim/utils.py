from .types import Position


def manhattan_distance(a: Position, b: Position) -> float:
    return abs(a.x - b.x) + abs(a.y - b.y)
