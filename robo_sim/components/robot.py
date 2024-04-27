import math
from abc import abstractmethod

from ..utils import Direction, Position
from .env import Env
from .env_objects import EnvObject
from .sensors import SensorInterface


class Robot(EnvObject):
    def __init__(self, pos: Position, speed: float) -> None:
        self.pos = pos
        self.speed = speed
        self.prev_pos = self.pos

    @property
    def radius(self):
        return 0.3

    @property
    def color(self):
        return "blue"

    @abstractmethod
    def move(self, direction: Direction, env: Env) -> None:
        """Move the robot in the specified direction within the evironment.

        Parameters
        ----------
        direction : Direction
            Direction in which to move.
        env : Env
            Environment the robot is using.
        """
        raise NotImplementedError()

    def move_to(self, new_pos: Position) -> None:
        """Update the robot's position to a new position.

        Parameters
        ----------
        new_pos : Position
            New position to move to.
        """
        self.prev_pos = self.pos
        self.pos = new_pos

    def check_collision_at_position(
        self, pos: Position, objs: list[EnvObject]
    ) -> bool:
        orig_position = self.pos
        self.pos = pos
        collision = self.check_collision(objs)
        self.pos = orig_position
        return collision

    def check_collision(self, objs: list[EnvObject]) -> bool:
        return any(self.object_within_range(obj) for obj in objs)


class BasicRobot(Robot):
    def move(self, direction: Direction, env: Env) -> None:
        """Move the robot in the specified direction within the evironment.

        Parameters
        ----------
        direction : Direction
            Direction in which to move.
        env : Env
            Environment the robot is using.
        """
        vec = Position(
            direction.value[0] * self.speed, direction.value[1] * self.speed
        )
        new_pos = self.pos + vec
        if env.is_within_bounds(new_pos) and not env.is_obstacle_in_range(
            new_pos, self.radius
        ):
            self.move_to(new_pos)


class SensorRobot(Robot):
    def __init__(
        self,
        pos: Position,
        speed: float,
        sensor: SensorInterface,
    ) -> None:
        super().__init__(pos, speed)
        self.sensor = sensor

    def move(self, direction: Direction, env: Env) -> None:
        """Move the robot in the specified direction within the evironment.

        Parameters
        ----------
        direction : Direction
            Direction in which to move.
        env : Env
            Environment the robot is using.
        """
        vec = Position(
            direction.value[0] * self.speed, direction.value[1] * self.speed
        )
        new_pos = self.pos + vec
        if env.is_within_bounds(new_pos) and not env.is_obstacle_in_range(
            new_pos, self.radius
        ):
            self.move_to(new_pos)

    def move_with_angle(self, angle: float, env: Env) -> None:
        """Move the robot based on an angle rather than a direction vector.

        Parameters
        ----------
        angle : float
            Angle in degrees to move.
        env : Env
            Environment the robot is using.
        """
        rad = math.radians(angle)
        dx = math.cos(rad) * self.speed
        dy = math.sin(rad) * self.speed
        new_pos = self.pos + (dx, dy)

        if env.is_within_bounds(new_pos) and not env.is_obstacle_in_range(
            new_pos, self.radius
        ):
            self.move_to(new_pos)

    def decide_move(self, env: Env) -> Position:
        """Decide the next move based on sensor data.

        Parameters
        ----------
        env : Env
            Environment the robot is using.

        Returns
        -------
        Position
            New position based on the best sensed direction.
        """
        sensor_data = self.sensor.sense(env, self.pos, self.radius)
        best_angle = max(sensor_data, key=sensor_data.get)
        rad = math.radians(best_angle)
        dx = math.cos(rad) * self.speed
        dy = math.sin(rad) * self.speed
        return self.pos + (dx, dy)
