from dataclasses import dataclass
from enum import Enum

from .grid import Grid


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


@dataclass
class Robot:
    pos: tuple[int, int]

    def move(self, direction: Direction, grid: Grid) -> None:
        dx, dy = direction.value
        new_pos = (self.pos[0] + dx, self.pos[1] + dy)

        if grid.update_robot_pos(self.pos, new_pos):
            self.pos = new_pos


@dataclass
class SensorRobot(Robot):
    sensor_range: int = 3

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
                check_pos = (self.pos[0] + i * dx, self.pos[1] + i * dy)
                if not grid.is_within_bounds(check_pos) or grid.is_obstacle(
                    check_pos
                ):
                    sensor_readings[d_name] = i
                    break

        return sensor_readings
