from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from ..components.env_objects import Target
from ..utils import Position

if TYPE_CHECKING:
    from ..components import Env, Robot
    from ..config import AlgorithmConfig


class Algorithm(ABC):
    def __init__(
        self,
        env: "Env",
        robot: "Robot",
        start: Position,
        target: Target,
        params: "AlgorithmConfig",
    ) -> None:
        self.env = env
        self.robot = robot
        self.start = start
        self.target = target
        self.params = params

    @abstractmethod
    def step(self) -> tuple[Position, float] | None:
        """Make a single step decision based on the current environment state.

        Returns
        -------
        tuple[Position |float] | None
            The new position and the orientation.
        """
        raise NotImplementedError()
