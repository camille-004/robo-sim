from pathlib import Path

from robo_sim.components import Env, Renderer, Summarizer, get_robot

from .algorithms import AlgorithmFactory, AlgorithmType
from .config import ConfigFactory
from .logging import get_logger
from .utils import Position

logger = get_logger(__name__)


class Sim:
    def __init__(self, config_path: Path, algorithm: str) -> None:
        logger.debug("Initializing simulation...")
        self.config = ConfigFactory(config_path).load()
        self.env = Env(
            size=self.config.env_size, obstacles=self.config.obstacles
        )
        self.robot = get_robot(self.config).create()
        self.target = self.config.target_pos
        self.env.set_target(self.target)
        algorithm_type = getattr(AlgorithmType, algorithm)
        self.algorithm = AlgorithmFactory.get_algorithm(
            algorithm_type,
            self.env,
            self.robot,
            self.config.start_pos,
            self.env.target,
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
        self.summarizer = Summarizer(self, self.robot, self.env)

        self.path: list[Position] = []
        self.step_idx = 0
        self.reached = False
        logger.debug("Simulation initialized.")

    def run(self) -> None:
        self.summarizer.start()
        while not self.reached:
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
