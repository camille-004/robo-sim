from enum import Enum
from typing import NamedTuple, Union


class Position(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Union[tuple, "Position"]) -> "Position":
        if isinstance(other, tuple) and len(other) == 2:
            return Position(self.x + other[0], self.y + other[1])
        elif isinstance(other, Position):
            return Position(self.x + other.x, self.y + other.y)
        else:
            raise ValueError("Can only add tuples of length 2 to Position.")

    def __sub__(self, other: Union[tuple, "Position"]) -> "Position":
        if isinstance(other, tuple) and len(other) == 2:
            return Position(self.x - other[0], self.y - other[1])
        elif isinstance(other, Position):
            return Position(self.x - other.x, self.y - other.y)
        else:
            raise ValueError(
                "Can only subtract tuples of length 2 from Position."
            )


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
