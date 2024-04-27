import random
from typing import TYPE_CHECKING

from ..logging import get_logger
from ..utils import Position
from .env_objects import EnvObject, EnvObjectFactory, Obstacle

if TYPE_CHECKING:
    from .robot import Robot

logger = get_logger(__name__)


class Env:
    def __init__(
        self,
        size: tuple[int, int] = (10, 10),
        obstacles: int | set[Position] = 0,
    ) -> None:
        self.size = size
        self.objects: list[EnvObject] = []

        if isinstance(obstacles, set):
            for pos in obstacles:
                self.add_object("obstacle", pos)
        elif isinstance(obstacles, int):
            self.generate_random_obstacles(obstacles)

    def add_object(self, object_type: str, pos: Position):
        if self.is_within_bounds(pos):
            obj = EnvObjectFactory.create(object_type, pos)
            if object_type == "target":
                self.target = obj
            self.objects.append(obj)
        else:
            raise ValueError("Position out of bounds.")

    def is_within_bounds(self, pos: Position) -> bool:
        return 0 <= pos.x <= self.size[0] and 0 <= pos.y <= self.size[1]

    def set_target(self, pos: Position) -> None:
        if self.is_within_bounds(pos):
            self.add_object("target", pos)
            logger.info(f"Target set at {pos}.")
        else:
            raise ValueError("Target position is out of env bounds.")

    def get_target(self) -> Position | None:
        return self.target.pos if self.target else None

    def is_obstacle_in_range(self, pos: Position, other_radius: float) -> bool:
        return any(
            obj.position_within_range(pos, other_radius)
            and isinstance(obj, Obstacle)
            for obj in self.objects
        )

    def robot_within_reach(self, robot: "Robot", obj: EnvObject) -> bool:
        return robot.object_within_range(obj)

    def generate_random_obstacles(self, num_obstacles: int) -> None:
        count = 0
        while count < num_obstacles:
            x = random.randint(0, self.size[0] - 1)
            y = random.randint(0, self.size[1] - 1)
            pos = Position(x, y)
            self.add_object("obstacle", pos)
            count += 1

    @property
    def obstacles(self) -> set[Obstacle]:
        return {obj for obj in self.objects if isinstance(obj, Obstacle)}
