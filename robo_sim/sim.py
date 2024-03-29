import logging
import random
from pathlib import Path

from .config import ConfigFactory
from .factory import BasicRobotFactory, registry
from .grid import Grid
from .renderer import Renderer
from .robot import Direction

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s"
)


def get_next_direction() -> Direction:
    """Placeholder: Randomly select the next direction."""
    return random.choice(list(Direction))


class Sim:
    def __init__(self, config_path: Path) -> None:
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
        self.renderer = Renderer(self.grid, grid_size=self.config.grid_size)

    def update(self) -> bool:
        if self.reached:
            return False

        if self.step >= self.steps:
            logging.info("Maximum number of steps reached.")
            return False

        direction = get_next_direction()
        self.robot.move(direction, self.grid)

        logging.info(f"Robot moved to {self.robot.pos}.")

        self.step += 1

        if self.robot.pos == self.target:
            logging.info("Target reached!")
            self.reached = True
            return False
        return True

    def run(self) -> None:
        self.renderer.animate(self, self.steps)
