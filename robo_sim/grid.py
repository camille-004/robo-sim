import numpy as np


class CellType:
    EMPTY = 0
    OBSTACLE = 1
    ROBOT = 2
    TARGET = 3


class Grid:
    def __init__(self, size: tuple[int, int] = (10, 10)) -> None:
        self.size = size
        self.grid = np.full(size, CellType.EMPTY, dtype=int)

    def add_obstacle(self, pos: tuple[int, int]) -> None:
        self.grid[pos] = CellType.OBSTACLE

    def add_target(self, pos: tuple[int, int]) -> None:
        self.grid[pos] = CellType.TARGET

    def is_obstacle(self, pos: tuple[int, int]) -> bool:
        return self.grid[pos] == CellType.OBSTACLE

    def is_within_bounds(self, pos: tuple[int, int]) -> bool:
        x, y = pos
        return 0 <= x < self.size[0] and 0 <= y < self.size[1]

    def update_robot_pos(
        self, old_pos: tuple[int, int], new_pos: tuple[int, int]
    ) -> bool:
        if self.is_within_bounds(new_pos) and not self.is_obstacle(new_pos):
            self.grid[old_pos] = CellType.EMPTY
            self.grid[new_pos] = CellType.ROBOT
            return True
        return False

    @property
    def obstacles(self) -> list[tuple[int, int]]:
        return [
            (x, y)
            for x in range(self.size[0])
            for y in range(self.size[1])
            if self.grid[x, y] == CellType.OBSTACLE
        ]
