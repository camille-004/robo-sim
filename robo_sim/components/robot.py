import math
from abc import abstractmethod

from ..utils import Direction, Position
from .env import Env
from .env_objects import EnvObject
from .sensors import SensorInterface


class Robot(EnvObject):
    def __init__(
        self,
        pos: Position,
        init_vel: float,
        init_ang_vel: float,
        orientation: float,
    ) -> None:
        self.pos = pos
        self.init_vel = init_vel
        self.init_ang_vel = init_ang_vel
        self.orientation = orientation
        self.prev_pos = self.pos

    @property
    def radius(self) -> float:
        return 0.3

    @property
    def color(self) -> str:
        return "blue"

    @property
    def shape(self) -> str:
        return "circle"

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

    def rotate_to(self, new_orientation: float) -> None:
        """Rotate the robot to a specific orientation

        Parameters
        ----------
        new_orientation : float
            The new orientation in degeres
        """
        self.orientation = new_orientation % 360

    def rotate_by(self, angle: float) -> None:
        """Rotate the robot by a given angle.

        Parameters
        ----------
        angle : float
            The angle in degrees to rotate by.
        """
        self.orientation = (self.orientation + angle) % 360


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
            direction.value[0] * self.init_vel,
            direction.value[1] * self.init_vel,
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
        init_vel: float,
        init_ang_vel: float,
        orientation: float,
        sensor: SensorInterface,
    ) -> None:
        super().__init__(pos, init_vel, init_ang_vel, orientation)
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
            direction.value[0] * self.init_vel,
            direction.value[1] * self.init_vel,
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
        dx = math.cos(rad) * self.init_vel
        dy = math.sin(rad) * self.init_vel
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
        dx = math.cos(rad) * self.init_vel
        dy = math.sin(rad) * self.init_vel
        return self.pos + (dx, dy)
