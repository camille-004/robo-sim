import logging
import random
from pathlib import Path

from .algorithms import AlgorithmFactory, AlgorithmType
from .config import ConfigFactory
from .factory import BasicRobotFactory, registry
from .grid import Grid
from .renderer import Renderer
from .robot import Direction
from .logging import get_logger


logger = get_logger(__name__)

class Sim:
    def __init__(
        self, config_path: Path, algorithm_type: AlgorithmType
    ) -> None:
        self.config = ConfigFactory(config_path).load()
        robot_factory = registry.get(type(self.config), BasicRobotFactory())
        self.robot = robot_factory.create_robot(self.config)
        self.grid = Grid(size=self.config.grid_size)
        self.algorithm = AlgorithmFactory.get_algorithm(
            algorithm_type,
            self.grid,
            self.config.start_pos,
            self.config.target_pos,
        )

        self.target = self.config.target_pos
        self.steps = self.config.steps

        self.step = 0
        self.reached = False

        self.grid.add_target(self.target)
        for obstacle in self.config.obstacles:
            self.grid.add_obstacle(obstacle)
        self.renderer = Renderer(self.grid, grid_size=self.config.grid_size)

    def plan_path(self) -> None:
        logger.debug("Executing path planning...")
        self.path = self.algorithm.exec()
        if self.path[0] == self.config.start_pos:
            self.path.pop(0)
        self.path_idx = 0

    def get_next_direction(self) -> Direction:
        if self.path and self.path_idx < len(self.path):
            next_pos = self.path[self.path_idx]
            self.path_idx += 1
            dx = next_pos[0] - self.robot.pos[0]
            dy = next_pos[1] - self.robot.pos[1]
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
            return False
        return True

    def run(self) -> None:
        self.renderer.animate(self, self.steps)
