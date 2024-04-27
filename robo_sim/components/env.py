import math
import random

from ..logging import get_logger
from ..utils import Position

logger = get_logger(__name__)


class Env:
    def __init__(
        self,
        size: tuple[int, int] = (10, 10),
        obstacles: int | set[Position] = 0,
    ) -> None:
        self.size = size
        self._obstacles: set[Position] = set()

        if isinstance(obstacles, set):
            for pos in obstacles:
                self.set_obstacle(pos)
        elif isinstance(obstacles, int):
            self.generate_random_obstacles(obstacles)

    def is_within_bounds(self, pos: Position) -> bool:
        return 0 <= pos.x <= self.size[0] and 0 <= pos.y <= self.size[1]

    def set_target(self, pos: Position) -> None:
        if self.is_within_bounds(pos):
            self.target = pos
            logger.info(f"Target set at {pos}.")
        else:
            raise ValueError("Target position is out of env bounds.")

    def set_obstacle(self, pos: Position | tuple[int, int]) -> None:
        if isinstance(pos, tuple):
            pos = Position(*pos)
        if self.is_within_bounds(pos):
            self._obstacles.add(pos)
        else:
            raise ValueError("Obstacle position is out of env bounds.")

    def is_obstacle(self, pos: Position) -> bool:
        return pos in self._obstacles

    def generate_random_obstacles(self, num_obstacles: int) -> None:
        count = 0
        while count < num_obstacles:
            x = random.randint(0, self.size[0] - 1)
            y = random.randint(0, self.size[1] - 1)
            pos = Position(x, y)
            if not self.is_obstacle(pos):
                self.set_obstacle(pos)
                count += 1

    def check_obstacle_in_direction(
        self, pos: Position, angle: float, rng: int
    ) -> bool:
        rad = math.radians(angle)
        for r in range(1, rng + 1):
            dx = r * math.cos(rad)
            dy = r * math.sin(rad)
            check_pos = pos + (dx, dy)
            if not self.is_within_bounds(check_pos) or self.is_obstacle(
                check_pos
            ):
                return True
        return False

    @property
    def obstacles(self) -> set[Position]:
        return self._obstacles
