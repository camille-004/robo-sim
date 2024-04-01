import pytest

from robo_sim.algorithms.pathfinding.astar import AStar
from robo_sim.components import Grid
from robo_sim.utils.types import Position
from robo_sim.utils.utils import manhattan_distance


@pytest.fixture
def empty_grid() -> Grid:
    return Grid(size=(5, 5), obstacles=[])


@pytest.fixture()
def grid_with_obstacles() -> Grid:
    obstacles = [Position(2, 2), Position(2, 3)]
    return Grid(size=(5, 5), obstacles=obstacles)


@pytest.fixture()
def grid_for_sensor_test() -> Grid:
    obstacles = [Position(2, 1), Position(2, 2), Position(2, 3)]
    return Grid(size=(5, 5), obstacles=obstacles)


def test_astar_pathfinding_emptpy_grid(empty_grid: Grid) -> None:
    start = Position(0, 0)
    target = Position(4, 4)
    astar = AStar(grid=empty_grid, start=start, target=target)

    path = astar.exec()

    assert path[0] == start
    assert path[-1] == target
    assert len(path) > 0


def test_astar_no_path_due_to_obstacles(grid_with_obstacles: Grid) -> None:
    start = Position(0, 0)
    target = Position(4, 4)
    astar = AStar(grid=grid_with_obstacles, start=start, target=target)

    path = astar.exec()

    assert path[0] == start
    assert path[-1] == target
    assert len(path) > 0
    assert len(path) > manhattan_distance(start, target)


def test_astar_sensor_range_adjustment(grid_for_sensor_test: Grid) -> None:
    start = Position(0, 0)
    target = Position(4, 4)
    sensor_range = 1
    astar_no_sensor = AStar(
        grid=grid_for_sensor_test, start=start, target=target
    )
    astar_sensor = AStar(
        grid=grid_for_sensor_test,
        start=start,
        target=target,
        sensor_range=sensor_range,
    )

    path_no_sensor = astar_no_sensor.exec()
    path_sensor = astar_sensor.exec()

    assert len(path_sensor) > 0
    assert path_sensor[0] == start
    assert path_sensor[-1] == target

    assert path_sensor != path_no_sensor

    assert len(path_sensor) >= len(path_no_sensor)

    print("Path with sensor range:")
    print(path_sensor)
    for pos in path_sensor:
        if not all(
            manhattan_distance(pos, obs) > sensor_range
            for obs in grid_for_sensor_test.obstacles
        ):
            print(f"Position too close to obstacle: {pos}")
            for obs in grid_for_sensor_test.obstacles:
                dist = manhattan_distance(pos, obs)
                print(f"Obstacle: {obs}, Distance: {dist}")
            assert (
                False
            ), f"Path includes positions too close to obstacles: {pos}"
