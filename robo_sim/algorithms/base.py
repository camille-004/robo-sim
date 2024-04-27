from abc import ABC, abstractmethod
from typing import Any

from ..components import Env, Robot
from ..utils import Position


class Algorithm(ABC):
    def __init__(
        self,
        env: Env,
        robot: Robot,
        start: Position,
        target: Position,
        sensor_range: int | None = None,
    ) -> None:
        self.env = env
        self.robot = robot
        self.start = start
        self.target = target
        self.sensor_range = sensor_range

    @abstractmethod
    def exec(self, *args: Any, **kwargs: Any) -> list[Position]:
        pass
