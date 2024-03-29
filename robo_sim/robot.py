from dataclasses import dataclass
from enum import Enum, auto

from .grid import Grid


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


@dataclass
class Robot:
    pos: tuple[int, int]

    def move(self, direction: Direction, grid: Grid) -> None:
        dx, dy = 0, 0
        match direction:
            case Direction.UP:
                dx = -1
            case Direction.DOWN:
                dx = 1
            case Direction.LEFT:
                dy = -1
            case Direction.RIGHT:
                dy = 1

        new_pos = (self.pos[0] + dx, self.pos[1] + dy)

        if grid.update_robot_pos(self.pos, new_pos):
            self.pos = new_pos
