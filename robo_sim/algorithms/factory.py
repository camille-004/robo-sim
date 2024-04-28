import importlib
from typing import TYPE_CHECKING

from robo_sim.components.env_objects import Target
from robo_sim.logging import get_logger
from robo_sim.utils import Position

from .base import Algorithm

if TYPE_CHECKING:
    from robo_sim.components import Env, Robot
    from robo_sim.config.config_models import AlgorithmConfig

logger = get_logger(__name__)


class AlgorithmFactory:
    @staticmethod
    def get_algorithm(
        env: "Env",
        robot: "Robot",
        start: Position,
        target: Target,
        params: "AlgorithmConfig",
    ) -> Algorithm:
        try:
            algorithm_type = params.__class__.__name__.replace("Config", "")
            module_name = algorithm_type.lower()
            class_name = algorithm_type
            module = importlib.import_module(
                f"robo_sim.algorithms.path_planning.{module_name}"
            )
            algorithm_class = getattr(module, class_name)
            return algorithm_class(
                env=env, robot=robot, start=start, target=target, params=params
            )
        except (AttributeError, ModuleNotFoundError) as e:
            logger.error(f"Algorithm {algorithm_type} not found: {e}.")
            raise ValueError(f"Algorithm {algorithm_type} not found.") from e
