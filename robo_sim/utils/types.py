from enum import Enum

from .utils import euclidean_distance


class Position:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: "tuple | Position | float") -> "Position":
        if isinstance(other, tuple) and len(other) == 2:
            return Position(self.x + other[0], self.y + other[1])
        elif isinstance(other, Position):
            return Position(self.x + other.x, self.y + other.y)
        elif isinstance(other, float):
            return Position(self.x + other, self.y + other)
        else:
            raise ValueError(
                "Can only add tuples of length 2, Positions, or floats to "
                "Position."
            )

    def __sub__(self, other: "tuple | Position | float") -> "Position":
        if isinstance(other, tuple) and len(other) == 2:
            return Position(self.x - other[0], self.y - other[1])
        elif isinstance(other, Position):
            return Position(self.x - other.x, self.y - other.y)
        elif isinstance(other, float):
            return Position(self.x - other, self.y - other)
        else:
            raise ValueError(
                "Can only subtract tuples of length 2, Positions, or floats "
                "from Position."
            )

    def __mul__(self, other: "Position | float") -> "Position":
        if isinstance(other, Position):
            return Position(self.x * other.x, self.y * other.y)
        elif isinstance(other, float):
            return Position(self.x * other, self.y * other)
        else:
            raise ValueError(
                "Can only multiply Positions or floats by Position."
            )

    def __truediv__(self, other: "Position | float") -> "Position":
        if isinstance(other, Position):
            if other.x == 0 or other.y == 0:
                raise ZeroDivisionError(
                    "Division by zero in element-wise division of Position."
                )
            return Position(self.x / other.x, self.y / other.y)
        elif isinstance(other, float):
            return Position(self.x / other, self.y / other)
        else:
            raise ValueError(
                "Can only divide Positions or floats by Position."
            )

    def euclidean_dist(self, other: "Position") -> float:
        return euclidean_distance(self, other)

    def __repr__(self) -> str:
        return f"Position(x={self.x}, y={self.y})"


class Direction(Enum):
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
