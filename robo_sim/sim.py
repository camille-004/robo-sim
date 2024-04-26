import random
from pathlib import Path

from .algorithms import AlgorithmFactory, AlgorithmType
from .components._robot_factory import get_robot
from .components.grid import Grid
from .components.renderer import Renderer
from .components.robot import Direction
from .components.summarizer import Summarizer
from .config import ConfigFactory
from .logging import get_logger
from .utils import Position

logger = get_logger(__name__)


class Sim:
    def __init__(self, config_path: Path, algorithm: str) -> None:
        self.config = ConfigFactory(config_path).load()
        self.robot = get_robot(self.config).create()
        self.grid = Grid(
            size=self.config.grid_size, obstacles=self.config.obstacles
        )

        self.target = self.config.target_pos
        self.steps = self.config.steps

        self.step = 0
        self.reached = False

        self.grid.set_target(self.target)
        logger.info("Grid initialized with target.")

        if not hasattr(AlgorithmType, algorithm):
            logger.error(f"No algorithm named '{algorithm}' found.")
            raise ValueError(f"No algorithm named '{algorithm}' available.")

        algorithm_type = getattr(AlgorithmType, algorithm)
        self.algorithm = AlgorithmFactory.get_algorithm(
            algorithm_type,
            self.grid,
            self.config.start_pos,
            self.target,
            (
                self.config.sensor.sensor_range
                if hasattr(self.config, "sensor")
                else None
            ),
        )
        self.renderer = Renderer(
            self.grid,
            trace_path=self.config.trace_path,
        )
        self.path: list[Position] = []
        self.path_idx = 0
        self.summarizer = Summarizer(self, self.robot, self.grid)

    def plan_path(self) -> None:
        logger.info("Executing path planning...")
        self.path = self.algorithm.exec()
        if self.path and self.path[0] == self.config.start_pos:
            self.path.pop(0)

    def get_next_direction(self) -> Direction:
        if self.path and self.path_idx < len(self.path):
            next_pos = self.path[self.path_idx]
            self.path_idx += 1
            dx = next_pos.x - self.robot.pos.x
            dy = next_pos.y - self.robot.pos.y

            if dx == 0 and dy == 0:
                raise ValueError(
                    "Next position is the same as current position."
                )

            return Direction((dx, dy))
        return random.choice(list(Direction))

    def update(self) -> bool:
        if self.reached:
            return False
        if self.step >= self.steps:
            logger.info("Maximum number of steps reached.")
            return False

        direction = self.get_next_direction()
        new_pos = self.robot.pos + direction.value

        if self.grid.is_within_bounds(new_pos) and not self.grid.is_obstacle(
            new_pos
        ):
            self.robot.move(direction, self.grid)
            self.step += 1
            logger.info(f"Robot moved to {self.robot.pos}.")
            if self.robot.pos == self.target:
                self.reached = True
                logger.info("Target reached!")

        return not self.reached

    def run(self) -> None:
        self.summarizer.start()
        self.plan_path()
        logger.info("Moving along path...")
        self.renderer.animate(self, self.steps)
        self.summarizer.end()
        self.summarizer.log_summary()
