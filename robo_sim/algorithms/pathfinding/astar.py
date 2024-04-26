import heapq
from typing import Any

from robo_sim.components import Grid
from robo_sim.utils import Position, manhattan_distance

from ..base import Algorithm
from .utils import compute_obstacle_proximity, get_proximity_penalty

PENALTY_FACTOR = 10


class AStar(Algorithm):
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
        open_set: list[tuple[float, int, Position, list[Any]]] = [
            (0, 0, self.start, [])
        ]
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

                proximity_penalty = get_proximity_penalty(
                    neighbor, self.obstacle_proximity_map, self.sensor_range
                )
                tentative_g_score = g_score[current] + 1 + proximity_penalty

                if tentative_g_score < g_score.get(neighbor, float("inf")):
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(neighbor)
                    heapq.heappush(
                        open_set, (f_score, count, neighbor, path + [current])
                    )
                    count += 1

        return []

    def heuristic(self, pos: Position) -> float:
        standard_heuristic = manhattan_distance(pos, self.target)
        if self.sensor_range is None:
            return standard_heuristic

        proximity_penalty = get_proximity_penalty(
            pos, self.obstacle_proximity_map, self.sensor_range
        )
        sensor_range_adjustment = self.sensor_range * PENALTY_FACTOR / 10
        return standard_heuristic + proximity_penalty + sensor_range_adjustment
