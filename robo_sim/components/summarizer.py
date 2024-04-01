import time
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..logging import get_logger
from ..utils.utils import manhattan_distance

if TYPE_CHECKING:
    from ..sim import Sim
    from .grid import Grid
    from .robot import Robot

logger = get_logger(__name__)


@dataclass
class SimStats:
    execution_time: float
    steps_taken: int
    path_length: int
    total_displacement: float
    sensor_readings_count: int | None


class Summarizer:
    def __init__(self, sim: "Sim", robot: "Robot", grid: "Grid") -> None:
        self.sim = sim
        self.robot = robot
        self.grid = grid
        self.start_pos = robot.pos

    def record_movement(self, distance: int) -> None:
        self.total_distance_traveled += distance

    def start(self):
        self.start_time = time.time()

    def end(self) -> None:
        self.end_time = time.time()
        self._calc_stats()

    def _calc_stats(self):
        exec_time = self.end_time - self.start_time if self.end_time else 0
        steps_taken = self.sim.step
        path_length = len(self.sim.path) if self.sim.path else 0
        sensor_readings_count = getattr(
            self.robot, "sensor_readings_count", None
        )

        total_displacement = manhattan_distance(self.robot.pos, self.start_pos)

        self.stats = SimStats(
            execution_time=exec_time,
            steps_taken=steps_taken,
            path_length=path_length,
            total_displacement=round(total_displacement, 2),
            sensor_readings_count=sensor_readings_count,
        )

    def log_summary(self) -> None:
        if not self.stats:
            logger.warning("No simulation stats available.")
            return

        logger.info("Simulation Summary:")
        logger.info(
            f"- Execution Time: {self.stats.execution_time:.2f} seconds"
        )
        logger.info(f"- Number of Steps Taken: {self.stats.steps_taken}")
        logger.info(f"- Planned Path Length: {self.stats.path_length}")
        logger.info(f"- Total Displacement: {self.stats.total_displacement}")

        if self.stats.sensor_readings_count is not None:
            logger.info(
                f"- Sensor Readings Used: {self.stats.sensor_readings_count}"
            )

        if self.sim.reached:
            logger.info("Target was successfully reached.")
        else:
            logger.warning(
                f"Target not reached Final position: {self.robot.pos}"
            )
