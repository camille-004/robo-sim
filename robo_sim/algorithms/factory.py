import importlib
from typing import Type

from robo_sim.grid import Grid
from robo_sim.logging import get_logger

from .base import Algorithm
from .types import AlgorithmType

logger = get_logger(__name__)


class AlgorithmFactory:
    @staticmethod
    def get_algorithm(
        algorithm_type: AlgorithmType,
        grid: Grid,
        start: tuple[int, int],
        target: tuple[int, int],
        sensor_range: int | None = None,
    ) -> Algorithm:
        try:
            module_name = algorithm_type.name.lower()
            class_name = algorithm_type.name
            module = importlib.import_module(
                f".pathfinding.{module_name}", "robo_sim.algorithms"
            )
            algorithm_class: Type[Algorithm] = getattr(module, class_name)
            return algorithm_class(grid, start, target, sensor_range)
        except (AttributeError, ModuleNotFoundError) as e:
            logger.error(f"Algorithm {algorithm_type.name} not found: {e}.")
            raise ValueError(f"Algorithm {algorithm_type} not found.") from e
