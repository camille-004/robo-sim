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


class CellType:
    EMPTY = "EMPTY"
    OBSTACLE = "OBSTACLE"
    ROBOT = "ROBOT"
    TARGET = "TARGET"


class Cell:
    def __init__(
        self,
        pos: Position,
        cell_type: CellType = CellType.EMPTY,
        reward: float | None = None,
    ) -> None:
        self.pos = pos
        self.cell_type = cell_type
        self.reward = reward

    def __repr__(self) -> str:
        return (
            f"Cell(position={self.pos},\n"
            + f"\tcell_type={self.cell_type},\n"
            + f"\treward={self.reward})\n"
        )

    def is_obstacle(self) -> bool:
        return self.cell_type == CellType.OBSTACLE

    def is_target(self) -> bool:
        return self.cell_type == CellType.TARGET


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
