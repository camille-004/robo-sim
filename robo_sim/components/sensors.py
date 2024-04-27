import math
from abc import ABC, abstractmethod
from typing import Any

from ..utils import Position
from .env import Env


class SensorInterface(ABC):
    @abstractmethod
    def sense(self, env: Env, pos: Position) -> Any:
        pass


class ProximitySensor(SensorInterface):
    def __init__(self, sensor_range: int) -> None:
        self.sensor_range = sensor_range
        self.sensor_readings_count = 0

    @abstractmethod
    def sense(self, env: Env, pos: Position) -> Any:
        pass


class BasicProximitySensor(ProximitySensor):
    def __init__(self, sensor_range: int):
        super().__init__(sensor_range)

    def sense_at_angle(self, env: Env, pos: Position, angle: float) -> float:
        rad = math.radians(angle)
        for r in range(1, self.sensor_range + 1):
            dx = int(r * math.cos(rad))
            dy = int(r * math.sin(rad))
            check_pos = pos + (dx, dy)

            if not env.is_within_bounds(check_pos) or env.is_obstacle(
                check_pos
            ):
                return math.sqrt(dx**2 + dy**2)

        return float(self.sensor_range)

    def sense(self, env: Env, pos: Position) -> dict[int, float]:
        angle_step = 5
        return {
            angle: self.sense_at_angle(env, pos, angle)
            for angle in range(0, 360, angle_step)
        }
