import random
from pathlib import Path

from .algorithms import AlgorithmFactory, AlgorithmType
from .config import ConfigFactory
from .factory import BasicRobotFactory, registry
from .grid import Grid
from .logging import get_logger
from .renderer import Renderer
from .robot import Direction
from .summarizer import Summarizer

logger = get_logger(__name__)


class Sim:
    def __init__(
        self, config_path: Path, algorithm_type: AlgorithmType
    ) -> None:
        self.config = ConfigFactory(config_path).load()
        robot_factory = registry.get(type(self.config), BasicRobotFactory())
        self.robot = robot_factory.create_robot(self.config)
        self.grid = Grid(size=self.config.grid_size)

        self.target = self.config.target_pos
        self.steps = self.config.steps

        self.step = 0
        self.reached = False

        self.grid.add_target(self.target)
        for obstacle in self.config.obstacles:
            self.grid.add_obstacle(obstacle)

        self.algorithm = AlgorithmFactory.get_algorithm(
            algorithm_type,
            self.grid,
            self.config.start_pos,
            self.config.target_pos,
            self.config.sensor_range if self.robot.has_sensor_data else None,
        )
        self.renderer = Renderer(self.grid, grid_size=self.config.grid_size)
        self.path = []
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
            dx = next_pos[0] - self.robot.pos[0]
            dy = next_pos[1] - self.robot.pos[1]

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
        self.robot.move(direction, self.grid)

        logger.info(f"Robot moved to {self.robot.pos}.")
        self.step += 1

        if self.robot.pos == self.target:
            logger.info("Target reached!")
            self.reached = True

        return not self.reached

    def run(self) -> None:
        self.summarizer.start()
        self.plan_path()
        logger.info("Moving along path...")
        self.renderer.animate(self, self.steps)
        self.summarizer.end()
        self.summarizer.log_summary()
