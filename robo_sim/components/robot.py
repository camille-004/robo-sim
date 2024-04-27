import math
from abc import ABC, abstractmethod
from typing import Any

from ..utils import Direction, Position
from .env import Env
from .sensors import SensorInterface


class Robot(ABC):
    def __init__(
        self, pos: Position, prev_pos: Position | None = None
    ) -> None:
        self.pos = pos
        self.prev_pos = prev_pos

    @abstractmethod
    def move(self, *args: Any, **kwargs: Any) -> None:
        pass


class BasicRobot(Robot):
    def move(self, direction: Direction, env: Env) -> None:
        new_pos = self.pos + direction.value
        if env.is_within_bounds(new_pos) and not env.is_obstacle(new_pos):
            self.prev_pos = self.pos
            self.pos = new_pos


class SensorRobot(Robot):
    def __init__(
        self,
        pos: Position,
        sensor: SensorInterface,
        prev_pos: Position | None = None,
    ) -> None:
        super().__init__(pos, prev_pos)
        self.sensor = sensor

    def move(self, angle: float, env: Env) -> None:
        rad = math.radians(angle)
        dx = math.cos(rad)
        dy = math.sin(rad)
        new_pos = self.pos + (dx, dy)

        if env.is_within_bounds(new_pos) and not env.is_obstacle(new_pos):
            self.prev_pos = self.pos
            self.pos = new_pos

    def decide_move(self, env: Env) -> float:
        sensor_data = self.sensor.sense(env, self.pos)
        best_angle = max(sensor_data, key=sensor_data.get)
        return best_angle
