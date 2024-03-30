import heapq

from robo_sim.grid import Grid
from robo_sim.logging import get_logger

from ..base import Algorithm

logger = get_logger(__name__)


PENALTY_FACTOR = 50


class AStar(Algorithm):
    def __init__(
        self,
        grid: Grid,
        start: tuple[int, int],
        target: tuple[int, int],
        sensor_range: int | None = None,
    ) -> None:
        self.grid = grid
        self.start = start
        self.target = target
        self.sensor_range = sensor_range
        self.obstacle_proximity_map = self.compute_obstacle_proximity()

    def exec(self) -> list[tuple[int, int]]:
        open_set = [(0, 0, self.start, [])]
        heapq.heapify(open_set)
        g_score = {self.start: 0}
        count = 1

        while open_set:
            _, _, current, path = heapq.heappop(open_set)

            if current == self.target:
                return path + [current]

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                neighbor = (current[0] + dx, current[1] + dy)

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

                    logger.debug(
                        f"g_score: {g_score[neighbor]}, f_score: {f_score}"
                    )

        return []

    def heuristic(self, pos: tuple[int, int]) -> int:
        standard_heuristic = abs(pos[0] - self.target[0]) + abs(
            pos[1] - self.target[1]
        )  # Manhattan distance.

        if self.sensor_range is None:
            return standard_heuristic

        proximity_penalty = self.get_proximity_penalty(pos)
        sensor_range_adjustment = self.sensor_range * PENALTY_FACTOR / 10
        return standard_heuristic + proximity_penalty + sensor_range_adjustment

    def get_proximity_penalty(self, pos: tuple[int, int]) -> int:
        if self.sensor_range is None:
            return 0
        proximity = self.obstacle_proximity_map.get(pos, self.sensor_range + 1)
        penalty = 0
        if proximity <= self.sensor_range:
            penalty = (
                (self.sensor_range - proximity + 1)
                * PENALTY_FACTOR
                * (self.sensor_range / 2)
            )
        return penalty

    def compute_obstacle_proximity(self) -> dict[tuple[int, int], int]:
        proximity_map = {}
        for x in range(self.grid.size[0]):
            for y in range(self.grid.size[1]):
                pos = (x, y)
                if self.grid.is_obstacle(pos):
                    proximity_map[pos] = 0
                else:
                    min_dist = min(
                        [
                            abs(x - ox) + abs(y - oy)
                            for ox, oy in self.grid.obstacles
                        ]
                    )
                    proximity_map[pos] = min_dist

        return proximity_map