from enum import Enum
from typing import NamedTuple


class Position(NamedTuple):
    x: float
    y: float

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

    def __truediv__(self, other: "tuple | Position | float") -> "Position":
        if isinstance(other, tuple) and len(other) == 2:
            return Position(self.x / other[0], self.y / other[1])
        elif isinstance(other, Position):
            return Position(self.x / other.x, self.y / other.y)
        elif isinstance(other, float):
            return Position(self.x / other, self.y / other)
        else:
            raise ValueError(
                "Can only divide tuples of length 2, Positions, or floats by "
                "Position."
            )


class Direction(Enum):
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
