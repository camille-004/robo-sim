import math
from dataclasses import dataclass, field

from ..utils import Direction, Position
from .grid import Grid


@dataclass
class Robot:
    pos: Position
    prev_pos: Position = field(init=False, default=None)

    def move(self, direction: Direction, grid: Grid) -> None:
        new_pos = self.pos + direction.value
        if grid.is_within_bounds(new_pos) and not grid.is_obstacle(new_pos):
            self.prev_pos = self.pos
            self.pos = new_pos


@dataclass
class SensorRobot(Robot):
    sensor_range: int
    sensor_readings_count: int = field(default=0, init=False)
    continuous_sensor: bool = False

    def sense_obstacles(self, grid: Grid) -> dict[str, int]:
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
                check_pos = self.pos + (i * dx, i * dy)
                self.sensor_readings_count += 1
                if not grid.is_within_bounds(check_pos):
                    sensor_readings[d_name] = i - 1
                    break
                if grid.is_obstacle(check_pos):
                    sensor_readings[d_name] = i
                    break

        return sensor_readings


@dataclass
class ContinuousSensorRobot(SensorRobot):
    continuous_sensor: bool = True

    def sense_obstacles(self, grid: Grid) -> float:
        min_distance = self.sensor_range

        for angle in range(0, 360, 5):
            rad = math.radians(angle)

            for r in range(1, self.sensor_range + 1):
                dx = int(r * math.cos(rad))
                dy = int(r * math.sin(rad))
                check_pos = self.pos + (dx, dy)

                self.sensor_readings_count += 1

                if not grid.is_within_bounds(check_pos):
                    distance = math.sqrt(dx**2 + dy**2)
                    min_distance = min(distance, distance - 1)
                    break

                if grid.is_obstacle(check_pos):
                    distance = math.sqrt(dx**2 + dy**2)
                    min_distance = min(distance, distance)
                    break

        return min_distance

    def sense_obstacle_at_angle(self, grid: Grid, angle: float) -> float:
        rad = math.radians(angle)
        min_distance = self.sensor_range

        for r in range(1, self.sensor_range + 1):
            dx = r * math.cos(rad)
            dy = r * math.sin(rad)

            check_pos_x = int(self.pos.x + dx)
            check_pos_y = int(self.pos.y + dy)
            check_pos = Position(check_pos_x, check_pos_y)

            self.sensor_readings_count += 1

            if not grid.is_within_bounds(check_pos) or grid.is_obstacle(
                check_pos
            ):
                distance = math.sqrt(dx**2 + dy**2)
                min_distance = min(min_distance, distance)
                break

        return min_distance
