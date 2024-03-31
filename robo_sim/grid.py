import random

import numpy as np

from .types import CellType, Position


class Grid:
    def __init__(
        self,
        size: tuple[int, int] = (10, 10),
        obstacles: int | list[Position] = 0,
    ) -> None:
        self.size = size
        self.grid = np.full(size, CellType.EMPTY, dtype=int)
        self.setup_obstacles(obstacles)

    def add_target(self, pos: Position) -> None:
        self.grid[pos.x, pos.y] = CellType.TARGET

    def is_obstacle(self, pos: Position) -> bool:
        return self.grid[pos.x, pos.y] == CellType.OBSTACLE

    def is_within_bounds(self, pos: Position) -> bool:
        return 0 <= pos.x < self.size[0] and 0 <= pos.y < self.size[1]

    def update_robot_pos(self, old_pos: Position, new_pos: Position) -> bool:
        if self.is_within_bounds(new_pos) and not self.is_obstacle(new_pos):
            self.grid[old_pos.x, old_pos.y] = CellType.EMPTY
            self.grid[new_pos.x, new_pos.y] = CellType.ROBOT
            return True
        return False

    def setup_obstacles(self, obstacles: int | list[tuple[int, int]]) -> None:
        if isinstance(obstacles, list):
            for pos in obstacles:
                self.add_obstacle(pos)
        elif isinstance(obstacles, int) and obstacles > 0:
            self.generate_random_obstacles(obstacles)

    def add_obstacle(self, pos: Position) -> None:
        self.grid[pos.x, pos.y] = CellType.OBSTACLE

    def generate_random_obstacles(
        self, num_obstacles: int, exclude: list[Position] = []
    ) -> None:
        count = 0
        while count < num_obstacles:
            x = random.randint(0, self.size[0] - 1)
            y = random.randint(0, self.size[1] - 1)
            if (x, y) not in exclude and self.grid[x, y] == CellType.EMPTY:
                self.add_obstacle(Position(x, y))
                count += 1

    @property
    def obstacles(self) -> list[Position]:
        return [
            Position(x, y)
            for x in range(self.size[0])
            for y in range(self.size[1])
            if self.grid[x, y] == CellType.OBSTACLE
        ]
