import importlib

from robo_sim.components import Env, Robot
from robo_sim.logging import get_logger
from robo_sim.utils import Position

from .base import Algorithm
from .enums import AlgorithmType

logger = get_logger(__name__)


class AlgorithmFactory:
    @staticmethod
    def get_algorithm(
        algorithm_type: AlgorithmType,
        env: Env,
        robot: Robot,
        start: Position,
        target: Position,
        sensor_range: int | None = None,
    ) -> Algorithm:
        try:
            module_name = algorithm_type.name.lower()
            class_name = algorithm_type.name
            module = importlib.import_module(
                f".path_planning.{module_name}", "robo_sim.algorithms"
            )
            algorithm_class: type[Algorithm] = getattr(module, class_name)
            return algorithm_class(env, robot, start, target, sensor_range)
        except (AttributeError, ModuleNotFoundError) as e:
            logger.error(f"Algorithm {algorithm_type.name} not found: {e}.")
            raise ValueError(f"Algorithm {algorithm_type} not found.") from e
