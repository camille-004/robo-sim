import math
from typing import Any

from robo_sim.components import Env, Robot
from robo_sim.utils import Position

from ..base import Algorithm


class Bug2(Algorithm):
    def __init__(
        self,
        env: Env,
        robot: Robot,
        start: Position,
        target: Position,
        sensor_range: int | None = None,
    ) -> None:
        super().__init__(env, robot, start, target, sensor_range)
        self.current_pos = start
        self.state = "towards_target"

    def exec(self, *args: Any, **kwargs: Any) -> list[Position]:
        path = [self.start]

        while self.current_pos != self.target:
            if self.state == "towards_target":
                next_pos = self.move_towards_target()
                if self.obstacle_detected(next_pos):
                    self.state = "follow_boundary"
                    path.append(self.current_pos)
                    continue
            elif self.state == "follow_boundary":
                next_pos = self.follow_boundary()
                if self.can_leave_boundary(next_pos):
                    self.state = "towards_target"

            self.current_pos = next_pos
            path.append(self.current_pos)
            if self.current_pos == self.target:
                break

        return path

    def move_towards_target(self) -> Position:
        direction = self.target - self.current_pos
        normalized_len = math.sqrt(direction.x**2 + direction.y**2)
        direction = direction / normalized_len
        next_pos = self.current_pos + direction
        return next_pos

    def obstacle_detected(self, pos: Position) -> bool:
        if hasattr(self.robot, "sensor"):
            sensor_data = self.robot.sensor.sense(self.env, pos)
            return any(dist < 1 for dist in sensor_data.values())
        else:
            return self.env.is_obstacle(pos)

    def follow_boundary(self) -> Position:
        raise NotImplementedError()

    def can_leave_boundary(self, pos: Position) -> bool:
        raise NotImplementedError()
