import math
from abc import ABC, abstractmethod
from typing import Any

from ..utils import Direction, Position
from .grid import Grid


class Robot(ABC):
    def __init__(
        self, pos: Position, prev_pos: Position | None = None
    ) -> None:
        self.pos = pos
        self.prev_pos = prev_pos

    @abstractmethod
    def move(self, direction: Direction, grid: Grid) -> None:
        pass


class BasicRobot(Robot):
    def move(self, direction: Direction, grid: Grid) -> None:
        new_pos = self.pos + direction.value
        if grid.is_within_bounds(new_pos) and not grid.is_obstacle(new_pos):
            self.prev_pos = self.pos
            self.pos = new_pos


class SensorInterface(ABC):
    @abstractmethod
    def sense(self, grid: Grid, pos: Position) -> Any:
        pass


class ObstacleSensor(SensorInterface):
    def __init__(self, sensor_range: int) -> None:
        self.sensor_range = sensor_range
        self.sensor_readings_count = 0

    def sense(self, grid: Grid, pos: Position) -> dict[str, int]:
        sensor_readings = {
            "UP": self.sensor_range,
            "DOWN": self.sensor_range,
            "LEFT": self.sensor_range,
            "RIGHT": self.sensor_range,
        }
        direction_names = {
            "UP": Direction.UP,
            "DOWN": Direction.DOWN,
            "RIGHT": Direction.RIGHT,
            "LEFT": Direction.LEFT,
        }

        for d_name, direction in direction_names.items():
            dx, dy = direction.value
            for i in range(1, self.sensor_range + 1):
                check_pos = pos + (i * dx, i * dy)
                self.sensor_readings_count += 1
                if not grid.is_within_bounds(check_pos):
                    sensor_readings[d_name] = i - 1
                    break
                if grid.is_obstacle(check_pos):
                    sensor_readings[d_name] = i
                    break

        return sensor_readings


class ContinuousObstacleSensor(SensorInterface):
    def __init__(self, sensor_range: int):
        self.sensor_range = sensor_range
        self.sensor_readings_count = 0

    def sense_at_angle(self, grid: Grid, pos: Position, angle: float) -> float:
        rad = math.radians(angle)
        for r in range(1, self.sensor_range + 1):
            dx = int(r * math.cos(rad))
            dy = int(r * math.sin(rad))
            check_pos = pos + (dx, dy)

            if not grid.is_within_bounds(check_pos) or grid.is_obstacle(
                check_pos
            ):
                return math.sqrt(dx**2 + dy**2)

        return float(self.sensor_range)

    def sense(self, grid: Grid, pos: Position) -> float:
        min_distance = float("inf")

        for angle in range(0, 360, 5):
            distance = self.sense_at_angle(grid, pos, angle)
            min_distance = min(min_distance, distance)

        return min_distance


class SensorRobot(BasicRobot):
    def __init__(
        self,
        pos: Position,
        sensor: SensorInterface,
        prev_pos: Position | None = None,
    ) -> None:
        super().__init__(pos, prev_pos)
        self.sensor = sensor

    def sense_obstacles(self, grid: Grid) -> dict[str, int]:
        return self.sensor.sense(grid, self.pos)


class ContinuousSensorRobot(SensorRobot):
    def __init__(
        self,
        pos: Position,
        sensor: SensorInterface,
        prev_pos: Position | None = None,
    ) -> None:
        super().__init__(pos, sensor, prev_pos)
