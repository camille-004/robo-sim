from enum import Enum
from typing import NamedTuple


class Position(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "tuple | Position") -> "Position":
        if isinstance(other, tuple) and len(other) == 2:
            return Position(self.x + other[0], self.y + other[1])
        elif isinstance(other, Position):
            return Position(self.x + other.x, self.y + other.y)
        else:
            raise ValueError("Can only add tuples of length 2 to Position.")

    def __sub__(self, other: "tuple | Position") -> "Position":
        if isinstance(other, tuple) and len(other) == 2:
            return Position(self.x - other[0], self.y - other[1])
        elif isinstance(other, Position):
            return Position(self.x - other.x, self.y - other.y)
        else:
            raise ValueError(
                "Can only subtract tuples of length 2 from Position."
            )


class Direction(Enum):
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
