import math
import random
from collections import deque

from robo_sim.components import BasicRobot, Env, Robot
from robo_sim.components.env_objects import Target
from robo_sim.logging import get_logger
from robo_sim.utils import Position

from ..base import Algorithm

logger = get_logger(__name__)


class BUG2(Algorithm):
    def __init__(
        self,
        env: Env,
        robot: Robot,
        start: Position,
        target: Target,
        sensor_range: int | None = None,
    ) -> None:
        super().__init__(env, robot, start, target, sensor_range)
        self.current_pos = start
        self.state = "towards_target"
        self.original_speed = robot.speed
        self.stuck_counter = 0
        self.escape_attempts = 0
        self.max_escape_attempts = 5
        self.last_boundary_contact_point = start
        self.last_positions: deque = deque(maxlen=10)
        self.stuck_detection_radius = self.robot.speed

    def step(self) -> Position | None:
        """Perform a single step in the BUG2 algorithm.

        Returns
        -------
        Position | None
            The next position decided by the algorithm.
        """
        if self.env.robot_within_reach(self.robot, self.target):
            return None

        next_pos = (
            self.move_towards_target()
            if self.state == "towards_target"
            else self.follow_boundary()
        )

        if self.state == "towards_target" and self.obstacle_detected(next_pos):
            self.state = "follow_boundary"
        elif self.state == "follow_boundary" and self.can_leave_boundary(
            next_pos
        ):
            self.state = "towards_target"

        self.last_positions.append(next_pos)
        if self.stuck():
            logger.warning(
                "Robot escaping from stuck position, picking random "
                + "direction that may override obstacle."
            )
            next_pos = self.escape()

        self.current_pos = next_pos
        return next_pos

    def stuck(self) -> bool:
        if len(self.last_positions) < 10:
            return False

        avg_x = sum(pos.x for pos in self.last_positions) / len(
            self.last_positions
        )
        avg_y = sum(pos.y for pos in self.last_positions) / len(
            self.last_positions
        )
        centroid = Position(avg_x, avg_y)

        return all(
            math.hypot(pos.x - centroid.x, pos.y - centroid.y)
            <= self.stuck_detection_radius
            for pos in self.last_positions
        )

    def escape(self) -> Position:
        directions = [
            (-self.robot.speed, 0),
            (self.robot.speed, 0),
            (0, -self.robot.speed),
            (0, self.robot.speed),
        ]
        random.shuffle(directions)
        for dx, dy in directions:
            new_pos = self.current_pos + (dx, dy)
            if self.env.is_within_bounds(
                new_pos
            ) and not self.env.is_obstacle_in_range(
                new_pos, self.robot.radius
            ):
                return new_pos
        return self.current_pos

    def move_towards_target(self) -> Position:
        """Compute the next position moving straight towards te target.

        Returns
        -------
        Position
            Next position moving towards the target.
        """
        direction = self.target.pos - self.current_pos
        step_size = self.robot.speed
        return (
            self.current_pos
            + (direction / math.hypot(direction.x, direction.y)) * step_size
        )

    def obstacle_detected(self, pos: Position) -> bool:
        """Check if there is an obstacle at the given position.

        Parameters
        ----------
        pos : Position
            Position at which to check for an obstacle.

        Returns
        -------
        bool
            Whether there is an obstacle at the given position.
        """
        if hasattr(self.robot, "sensor"):
            sensor_data = self.robot.sensor.sense(
                self.env, pos, self.robot.radius
            )

            for angle, distance in sensor_data.items():
                if distance < self.sensor_range:
                    rad_angle = math.radians(angle)
                    obstacle_pos = Position(
                        pos.x + distance * math.cos(rad_angle),
                        pos.y + distance * math.sin(rad_angle),
                    )
                    if self.env.is_obstacle_in_range(
                        obstacle_pos, self.robot.radius
                    ):
                        return True
        temp = BasicRobot(pos, self.robot.speed)
        return any(
            self.env.robot_within_reach(temp, obstacle)
            for obstacle in self.env.objects
        )

    def follow_boundary(self) -> Position:
        if hasattr(self.robot, "sensor"):
            return self.follow_with_sensor()
        return self.simple_boundary_follow()

    def follow_with_sensor(self) -> Position:
        if hasattr(self.robot, "sensor"):
            sensor_data = self.robot.sensor.sense(
                self.env, self.current_pos, self.robot.radius
            )
        safe_direction, max_clearance = max(
            sensor_data.items(), key=lambda x: x[1]
        )
        rad = math.radians(safe_direction)
        dx = math.cos(rad) * self.robot.speed
        dy = math.sin(rad) * self.robot.speed
        new_pos = self.current_pos + (dx, dy)
        logger.debug(f"Moving to new position {new_pos}.")

        return new_pos

    def simple_boundary_follow(self) -> Position:
        angle_options = range(360)
        for angle in angle_options:
            rad = math.radians(angle)
            dx = -self.robot.speed * math.sin(rad)
            dy = self.robot.speed * math.cos(rad)
            next_pos = self.current_pos + (dx, dy)
            if self.env.is_within_bounds(
                next_pos
            ) and not self.env.is_obstacle_in_range(
                next_pos, self.robot.radius
            ):
                return next_pos

        return self.current_pos

    def can_leave_boundary(self, pos: Position) -> bool:
        """Check if the robot can safely leave the boundary and continue moving
        towards the target.

        Parameters
        ----------
        pos : Position
            Current position of the robot.

        Returns
        -------
        bool
            True if the robot can start heading towards the target, False
            otherwise.
        """
        direction_to_target = self.target.pos - pos
        return math.hypot(
            direction_to_target.x, direction_to_target.y
        ) < math.hypot(
            self.last_boundary_contact_point.x - self.target.pos.x,
            self.last_boundary_contact_point.y - self.target.pos.y,
        )
