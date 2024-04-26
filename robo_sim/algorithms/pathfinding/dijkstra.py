import heapq
from typing import Any

from robo_sim.components import Grid
from robo_sim.utils import Position

from ..base import Algorithm
from .utils import compute_obstacle_proximity, get_proximity_penalty

PENALTY_FACTOR = 10


class Dijkstra(Algorithm):
    def __init__(
        self,
        grid: Grid,
        start: Position,
        target: Position,
        sensor_range: int | None = None,
    ) -> None:
        super().__init__(grid, start, target, sensor_range)
        self.obstacle_proximity_map = compute_obstacle_proximity(
            grid, sensor_range
        )

    def exec(self) -> list[Position]:
        open_set: list[tuple[int, Position, list[Any]]] = [(0, self.start, [])]
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
                    g_score[current]
                    + 1  # noqa
                    + get_proximity_penalty(  # noqa
                        neighbor,
                        self.obstacle_proximity_map,
                        self.sensor_range,
                    )
                )

                if tentative_g_score < g_score.get(neighbor, float("inf")):
                    g_score[neighbor] = tentative_g_score
                    heapq.heappush(
                        open_set,
                        (tentative_g_score, neighbor, path + [current]),
                    )

        return []
