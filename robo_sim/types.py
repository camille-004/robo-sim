from enum import Enum
from typing import NamedTuple


class Position(NamedTuple):
    x: int
    y: int


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


class CellType:
    EMPTY = 0
    OBSTACLE = 1
    ROBOT = 2
    TARGET = 3
