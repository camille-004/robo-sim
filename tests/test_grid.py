import pytest

from robo_sim.components import EmptyCell, Grid, ObstacleCell, TargetCell
from robo_sim.utils.types import Position


def test_grid_initialization() -> None:
    grid_size = (5, 5)
    grid = Grid(size=grid_size)

    assert grid.size == grid_size
    for cell in grid:
        assert isinstance(
            cell, EmptyCell
        ), "Grid should initialize with EmptyCells."


def test_obstacle_placement() -> None:
    grid = Grid(size=(5, 5))
    obstacles = [Position(1, 1), Position(2, 2)]

    for pos in obstacles:
        grid.set_obstacle(pos)

    for x in range(5):
        for y in range(5):
            if Position(x, y) in obstacles:
                assert isinstance(
                    grid[x, y], ObstacleCell
                ), f"Obstacle expected at {Position(x, y)}."
            else:
                assert not isinstance(
                    grid[x, y], ObstacleCell
                ), f"No obstacle expected at {Position(x, y)}."


def test_target_setting() -> None:
    grid = Grid(size=(5, 5))
    target_pos = Position(3, 3)
    grid.set_target(target_pos)

    assert isinstance(
        grid[target_pos.x, target_pos.y], TargetCell
    ), "Target cell not set correctly."


@pytest.mark.parametrize("num_obstacles", [5, 10, 15])
def test_random_obstacle_generation(num_obstacles: int) -> None:
    grid = Grid(size=(10, 10))
    grid.generate_random_obstacles(num_obstacles)

    obstacle_count = sum(
        isinstance(cell, ObstacleCell) for row in grid.grid for cell in row
    )
    assert (
        obstacle_count == num_obstacles
    ), f"Expected {num_obstacles} obstacles, found {obstacle_count}."
