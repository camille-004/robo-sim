from pathlib import Path

from .algorithms import AlgorithmFactory, AlgorithmType
from .components._robot_factory import get_robot
from .components.env import Env
from .components.renderer import Renderer
from .components.summarizer import Summarizer
from .config import ConfigFactory
from .logging import get_logger
from .utils import Position

logger = get_logger(__name__)


class Sim:
    def __init__(self, config_path: Path, algorithm: str) -> None:
        self.config = ConfigFactory(config_path).load()
        self.robot = get_robot(self.config).create()
        self.env = Env(
            size=self.config.env_size, obstacles=self.config.obstacles
        )

        self.target = self.config.target_pos
        self.steps = self.config.steps

        self.step = 0
        self.reached = False

        self.env.set_target(self.target)
        logger.info("Environment initialized with target.")

        if not hasattr(AlgorithmType, algorithm):
            logger.error(f"No algorithm named '{algorithm}' found.")
            raise ValueError(f"No algorithm named '{algorithm}' available.")

        algorithm_type = getattr(AlgorithmType, algorithm)
        self.algorithm = AlgorithmFactory.get_algorithm(
            algorithm_type,
            self.env,
            self.robot,
            self.config.start_pos,
            self.target,
            (
                self.config.sensor.sensor_range
                if hasattr(self.config, "sensor")
                else None
            ),
        )
        self.renderer = Renderer(
            self.env,
            trace_path=self.config.trace_path,
        )
        self.path: list[Position] = []
        self.path_idx = 0
        self.summarizer = Summarizer(self, self.robot, self.env)

    def plan_path(self) -> None:
        raise NotImplementedError()

    def update(self) -> bool:
        raise NotImplementedError()

    def run(self) -> None:
        self.summarizer.start()
        self.plan_path()
        logger.info("Moving along path...")
        self.renderer.animate(self, self.steps)
        self.summarizer.end()
        self.summarizer.log_summary()
