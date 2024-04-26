from abc import ABC, abstractmethod
from typing import Any

from ..components import Grid
from ..utils import Position


class Algorithm(ABC):
    def __init__(self, grid: Grid, start: Position, target: Position, sensor_range: int | None = None) -> None:
        self.grid = grid
        self.start = start
        self.target = target
        self.sensor_range = sensor_range

    @abstractmethod
    def exec(self, *args: Any, **kwargs: Any) -> list[Position]:
        pass
