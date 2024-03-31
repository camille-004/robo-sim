import random
from typing import Iterator

import numpy as np

from .types import Cell, CellType, Position


class Grid:
    def __init__(
        self,
        size: tuple[int, int] = (10, 10),
        obstacles: int | list[Position] = 0,
    ) -> None:
        self.size = size
        self.grid = np.array(
            [
                [Cell(Position(x, y)) for y in range(size[1])]
                for x in range(size[0])
            ]
        )

        self._obstacles = []

        if isinstance(obstacles, list):
            for pos in obstacles:
                self.set_obstacle(pos)
        elif isinstance(obstacles, int):
            self.generate_random_obstacles(obstacles)

    def __iter__(self) -> Iterator[Cell]:
        for row in self.grid:
            for cell in row:
                yield cell

    def is_within_bounds(self, pos: Position) -> bool:
        return 0 <= pos.x < self.size[0] and 0 <= pos.y < self.size[1]

    def set_target(self, pos: Position) -> None:
        if self.is_within_bounds(pos):
            self.grid[pos.x][pos.y].cell_type = CellType.TARGET
        else:
            raise ValueError("Target position is out of grid bounds.")

    def set_obstacle(self, pos: Position | tuple[int, int]) -> None:
        if isinstance(pos, tuple):
            pos = Position(*pos)
        if self.is_within_bounds(pos):
            self.grid[pos.x, pos.y].cell_type = CellType.OBSTACLE
            self._obstacles.append(pos)
        else:
            raise ValueError("Obstacle position is out of grid bounds.")

    def is_obstacle(self, pos: Position | tuple[int, int]) -> bool:
        if isinstance(pos, tuple):
            pos = Position(*pos)
        return self.grid[pos.x][pos.y].cell_type == CellType.OBSTACLE

    def update_robot_pos(self, old_pos: Position, new_pos: Position) -> bool:
        if self.is_within_bounds(new_pos) and not self.is_obstacle(new_pos):
            self.grid[old_pos.x, old_pos.y].cell_type = CellType.EMPTY
            self.grid[new_pos.x, new_pos.y].cell_type = CellType.ROBOT
            return True
        return False

    def generate_random_obstacles(self, num_obstacles: int) -> None:
        count = 0
        while count < num_obstacles:
            x = random.randint(0, self.size[0] - 1)
            y = random.randint(0, self.size[1] - 1)
            if not self.is_obstacle((x, y)):
                self.set_obstacle((x, y))
                count += 1

    @property
    def obstacles(self) -> list[Position]:
        return self._obstacles
