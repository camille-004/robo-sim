import heapq

from robo_sim.components import Grid
from robo_sim.utils import Position, manhattan_distance

from ..base import Algorithm

PENALTY_FACTOR = 10


class Dijkstra(Algorithm):
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
        open_set = [(0, self.start, [])]
        heapq.heapify(open_set)

        g_score = {self.start: 0}

        while open_set:
            current_cost, current, path = heapq.heappop(open_set)

            if current == self.target:
                return path + [current]

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                neighbor = current + (dx, dy)

                if not self.grid.is_within_bounds(
                    neighbor
                ) or self.grid.is_obstacle(neighbor):
                    continue

                tentative_g_score = (
                    g_score[current] + 1 + self.get_proximity_penalty(neighbor)
                )

                if tentative_g_score < g_score.get(neighbor, float("inf")):
                    g_score[neighbor] = tentative_g_score
                    heapq.heappush(
                        open_set,
                        (tentative_g_score, neighbor, path + [current]),
                    )

        return []

    def get_proximity_penalty(self, pos: Position) -> int:
        if self.sensor_range is None:
            return 0

        proximity = self.obstacle_proximity_map.get(pos, self.sensor_range + 1)
        penalty = (
            max(0, (self.sensor_range + 1 - proximity) ** 2) * PENALTY_FACTOR
        )
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
                if self.grid.is_obstacle(cell.pos):
                    proximity_map[cell.pos] = 0
                else:
                    min_dist = min(
                        manhattan_distance(cell.pos, obs)
                        for obs in self.grid.obstacles
                    )
                    proximity_map[cell.pos] = min_dist

        return proximity_map
