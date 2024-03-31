from dataclasses import dataclass, field

from ..utils.types import Direction, Position
from .grid import Grid


@dataclass
class Robot:
    pos: Position
    prev_pos: Position = field(init=False, default=None)
    sensor_range: int = field(default=None, repr=False)
    has_sensor_data: bool = field(default=False, init=False)

    def __post_init__(self):
        if self.sensor_range is not None:
            self.has_sensor_data = True

    def move(self, direction: Direction, grid: Grid) -> None:
        new_pos = self.pos + direction.value
        if grid.is_within_bounds(new_pos) and not grid.is_obstacle(new_pos):
            self.prev_pos = self.pos
            self.pos = new_pos
            return True
        return False


@dataclass
class SensorRobot(Robot):
    sensor_range: int = 3
    sensor_readings_count: int = field(default=0, init=False)

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
                if not grid.is_within_bounds(check_pos) or grid.is_obstacle(
                    check_pos
                ):
                    sensor_readings[d_name] = i
                    break

        return sensor_readings
