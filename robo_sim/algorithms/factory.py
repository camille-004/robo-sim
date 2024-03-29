import importlib
import logging
from typing import Any, Type

from .base import Algorithm
from .types import AlgorithmType

logger = logging.getLogger(__name__)


class AlgorithmFactory:
    @staticmethod
    def get_algorithm(
        algorithm_type: AlgorithmType, *args: Any, **kwargs: Any
    ) -> Algorithm:
        try:
            module_name = algorithm_type.name.lower()
            class_name = algorithm_type.name
            module = importlib.import_module(
                f".pathfinding.{module_name}", "robo_sim.algorithms"
            )
            algorithm_class: Type[Algorithm] = getattr(module, class_name)
            return algorithm_class(*args, **kwargs)
        except (AttributeError, ModuleNotFoundError) as e:
            logger.error(f"Algorithm {algorithm_type.name} not found: {e}.")
            raise ValueError(f"Algorithm {algorithm_type} not found.") from e
