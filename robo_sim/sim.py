from pathlib import Path

import numpy as np

from robo_sim.components import Env, Renderer, Summarizer, get_robot

from .algorithms import AlgorithmFactory
from .config import ConfigFactory
from .logging import get_logger
from .utils import Position

logger = get_logger(__name__)


class Sim:
    def __init__(
        self,
        env_config_path: Path,
        robot_config_path: Path,
        algorithm_config_path: Path,
    ) -> None:
        logger.debug("Initializing simulation...")
        config_factory = ConfigFactory(
            env_config_path, robot_config_path, algorithm_config_path
        )
        self.env_config = config_factory.load_env_config()
        self.robot_config = config_factory.load_robot_config()
        self.algorithm_config = config_factory.load_algorithm_config()
        self.env = Env(
            size=self.env_config.size, obstacles=self.env_config.obstacles
        )
        self.robot = get_robot(self.robot_config).create()
        self.target = self.env_config.target_pos
        self.start = self.robot_config.start_pos
        self.adjust_robot_start(self.start)
        self.env.set_target(self.target)
        self.algorithm = AlgorithmFactory.get_algorithm(
            env=self.env,
            robot=self.robot,
            start=self.start,
            target=self.env.target,
            params=self.algorithm_config,
        )
        self.renderer = Renderer(
            self.env,
            trace_path=self.env_config.trace_path,
        )
        self.summarizer = Summarizer(self, self.robot, self.env)

        self.path: list[Position] = []
        self.step_idx = 0
        self.reached = False
        logger.debug("Simulation initialized.")

    def run(self) -> None:
        self.summarizer.start()
        while not self.reached and self.step_idx < self.env_config.max_frames:
            next_pos = self.algorithm.step()
            if next_pos is None:
                logger.error("No more moves possible or target reached.")
                break
            self.robot.move_to(next_pos)
            self.renderer.animate_step_by_step(
                self, self.step_idx, self.reached
            )
            self.step_idx += 1
            self.reached = self.env.robot_within_reach(
                self.robot, self.env.target
            )

        self.renderer.animate_step_by_step(self, self.step_idx, True)
        self.summarizer.end()
        self.summarizer.log_summary()

    def adjust_robot_start(self, start_pos: Position):
        if self.env.is_obstacle_in_range(start_pos, self.robot.radius):
            logger.debug(
                "Obstacle within robot's chosen starting position. "
                "Adjusting robot's starting position..."
            )
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            for distance in np.arange(1, 2, 0.1):
                for dx, dy in directions:
                    new_pos = Position(
                        self.robot.pos.x + dx * distance,
                        self.robot.pos.y + dy * distance,
                    )
                    if self.env.is_within_bounds(
                        new_pos
                    ) and not self.env.is_obstacle_in_range(
                        new_pos, self.robot.radius
                    ):
                        self.robot.move_to(new_pos)
                        self.start = new_pos
                        logger.info(
                            f"Robot moved to starting position {new_pos}."
                        )
                        return
            raise RuntimeError(
                "Failed to find a suitable starting position in this "
                "environment."
            )
        logger.info("No adjustment needed for robot's starting position.")
