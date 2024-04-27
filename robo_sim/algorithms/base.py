from abc import ABC, abstractmethod

from ..components import Env, Robot
from ..components.env_objects import Target
from ..utils import Position


class Algorithm(ABC):
    def __init__(
        self,
        env: Env,
        robot: Robot,
        start: Position,
        target: Target,
        sensor_range: int | None = None,
    ) -> None:
        self.env = env
        self.robot = robot
        self.start = start
        self.target = target
        self.sensor_range = sensor_range

    @abstractmethod
    def step(self) -> Position | None:
        """Make a single step decision based on the current environment state.

        Returns
        -------
        Position | None
            The position of the next step to take.
        """
        raise NotImplementedError()
