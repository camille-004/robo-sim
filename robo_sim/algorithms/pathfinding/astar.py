import heapq

from robo_sim.grid import Grid
from robo_sim.logging import get_logger

from ..base import Algorithm

logger = get_logger(__name__)


class AStar(Algorithm):
    def __init__(
        self, grid: Grid, start: tuple[int, int], target: tuple[int, int]
    ) -> None:
        self.grid = grid
        self.start = start
        self.target = target

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

                tentative_g_score = g_score[current] + 1

                if tentative_g_score < g_score.get(neighbor, float("inf")):
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(
                        neighbor, self.target
                    )
                    heapq.heappush(
                        open_set, (f_score, count, neighbor, path + [current])
                    )
                    count += 1

                    logger.debug(
                        f"Neighbor: {neighbor}, g_score: {g_score[neighbor]}, f_score: {f_score}"
                    )

        return []

    def heuristic(self, pos: tuple[int, int], target: tuple[int, int]) -> int:
        return abs(pos[0] - target[0]) + abs(pos[1] - target[1])
