import heapq

from robo_sim.components import Grid
from robo_sim.logging import get_logger
from robo_sim.utils.types import Position
from robo_sim.utils.utils import manhattan_distance

from ..base import Algorithm

logger = get_logger(__name__)


PENALTY_FACTOR = 10


class AStar(Algorithm):
    def __init__(
        self,
        grid: Grid,
        start: Position,
        target: Position,
        sensor_range: int | None = None,
    ) -> None:
        self.grid = grid
        self.start = start
        self.target = target
        self.sensor_range = sensor_range
        self.obstacle_proximity_map = self.compute_obstacle_proximity()

    def exec(self) -> list[Position]:
        open_set = [(0, 0, self.start, [])]
        heapq.heapify(open_set)
        count = 1

        g_score: dict[Position, float] = {self.start: 0}

        while open_set:
            _, _, current, path = heapq.heappop(open_set)

            if current == self.target:
                return path + [current]

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                neighbor = current + (dx, dy)

                if not self.grid.is_within_bounds(
                    neighbor
                ) or self.grid.is_obstacle(neighbor):
                    continue

                proximity_penalty = self.get_proximity_penalty(neighbor)
                tentative_g_score = g_score[current] + 1 + proximity_penalty

                if tentative_g_score < g_score.get(neighbor, float("inf")):
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(neighbor)
                    heapq.heappush(
                        open_set, (f_score, count, neighbor, path + [current])
                    )
                    count += 1

        return []

    def heuristic(self, pos: Position) -> int:
        standard_heuristic = manhattan_distance(pos, self.target)
        if self.sensor_range is None:
            return standard_heuristic

        proximity_penalty = self.get_proximity_penalty(pos)
        sensor_range_adjustment = self.sensor_range * PENALTY_FACTOR / 10
        return standard_heuristic + proximity_penalty + sensor_range_adjustment

    def get_proximity_penalty(self, pos: Position) -> int:
        if self.sensor_range is None:
            return 0

        proximity = self.obstacle_proximity_map.get(pos, self.sensor_range + 1)
        penalty = 0
        if proximity <= self.sensor_range:
            penalty = (self.sensor_range - proximity + 1) ** 2 * PENALTY_FACTOR
        return penalty

    def compute_obstacle_proximity(self) -> dict[Position, int]:
        proximity_map: dict[Position, float] = {}

        if not self.grid.obstacles:
            safe_distance = (
                self.sensor_range + 1 if self.sensor_range is not None else 0
            )
            for cell in self.grid:
                proximity_map[cell.pos] = safe_distance
        else:
            for cell in self.grid:
                if self.grid.is_obstacle(cell):
                    proximity_map[cell.pos] = 0
                else:
                    min_dist = min(
                        abs(cell.pos.x - obs.x) + abs(cell.pos.y - obs.y)
                        for obs in self.grid.obstacles
                    )
                    proximity_map[cell.pos] = min_dist

        return proximity_map
