import numpy as np

from robo_sim.components.env import Env
from robo_sim.components.env_objects import Target
from robo_sim.components.robot import Robot
from robo_sim.config.config_models import RRTConfig
from robo_sim.logging import get_logger
from robo_sim.utils import Position

from ..base import Algorithm

logger = get_logger(__name__)


class RRT(Algorithm):
    params: RRTConfig

    def __init__(
        self,
        env: Env,
        robot: Robot,
        start: Position,
        target: Target,
        params: RRTConfig,
    ) -> None:
        super().__init__(env, robot, start, target, params)
        self.tree = [start]

    def distance(self, a: Position, b: Position) -> float:
        return np.hypot(b.x - a.x, b.y - a.y)

    def steer(self, from_node: Position, to_node: Position) -> Position:
        theta = np.arctan2(to_node.y - from_node.y, to_node.x - from_node.x)
        new_pos = Position(
            from_node.x + self.params.max_step_size * np.cos(theta),
            from_node.y + self.params.max_step_size * np.sin(theta),
        )
        logger.debug(f"Steering from {from_node} to {new_pos}")
        return new_pos

    def collision_free(self, node: Position) -> bool:
        return not self.env.is_obstacle_in_range(node, self.robot.radius)

    def nearest_node(self, new_node: Position) -> Position:
        return min(self.tree, key=lambda node: self.distance(node, new_node))

    def step(self) -> tuple[Position, float] | None:
        for i in range(self.params.max_iter):
            random_point = (
                self.target.pos
                if np.random.rand() > self.params.goal_sample_rate / 100
                else Position(
                    np.random.uniform(0, self.env.size[0]),
                    np.random.uniform(0, self.env.size[1]),
                )
            )
            nearest = self.nearest_node(random_point)
            new_pos = self.steer(nearest, random_point)

            if self.collision_free(new_pos):
                self.tree.append(new_pos)
                logger.debug(f"Node added at {new_pos}.")
                if (
                    self.distance(new_pos, self.target.pos)
                    < self.params.max_step_size
                ):
                    logger.info("Goal reached.")
                    return new_pos, 0
            else:
                logger.debug(f"Collision detected at {new_pos}.")

        return None
