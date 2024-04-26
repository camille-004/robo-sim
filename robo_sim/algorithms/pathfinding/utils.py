from robo_sim.components import Grid
from robo_sim.utils import Position, manhattan_distance

PENALTY_FACTOR = 10


def compute_obstacle_proximity(
    grid: Grid, sensor_range: int | None = None
) -> dict[Position, int]:
    proximity_map: dict[Position, int] = {}

    if not grid.obstacles:
        safe_distance = sensor_range + 1 if sensor_range is not None else 0
        for cell in grid:
            proximity_map[cell.pos] = safe_distance
    else:
        for cell in grid:
            if grid.is_obstacle(cell.pos):
                proximity_map[cell.pos] = 0
            else:
                min_dist = min(
                    manhattan_distance(cell.pos, obs) for obs in grid.obstacles
                )
                proximity_map[cell.pos] = int(min_dist)

    return proximity_map


def get_proximity_penalty(
    pos: Position,
    obstacle_proximity_map: dict[Position, int],
    sensor_range: int | None,
) -> int:
    if sensor_range is None or not obstacle_proximity_map:
        return 0

    proximity = obstacle_proximity_map.get(pos, sensor_range + 1)
    penalty = int(max(0, (sensor_range + 1 - proximity) ** 2) * PENALTY_FACTOR)
    return penalty
