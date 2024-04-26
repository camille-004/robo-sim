import pytest

from robo_sim.components import BasicRobot, Grid, ObstacleSensor, SensorRobot
from robo_sim.utils import Direction, Position


def test_robot_init() -> None:
    start_pos = Position(1, 1)
    robot = BasicRobot(pos=start_pos)

    assert (
        robot.pos == start_pos
    ), "Robot did not initialize at the correct position."


@pytest.mark.parametrize(
    "direction, expected_position",
    [
        (Direction.UP, Position(1, 2)),
        (Direction.DOWN, Position(1, 0)),
        (Direction.LEFT, Position(0, 1)),
        (Direction.RIGHT, Position(2, 1)),
    ],
)
def test_robot_movement(
    direction: Direction, expected_position: Position
) -> None:
    start_pos = Position(1, 1)
    grid = Grid(size=(3, 3))
    robot = BasicRobot(pos=start_pos)

    robot.move(direction, grid)

    assert (
        robot.pos == expected_position
    ), f"Robot did not move correctly to {expected_position}."


def test_robot_blocked_by_obstacle() -> None:
    start_pos = Position(1, 1)
    grid = Grid(size=(3, 3), obstacles=[Position(1, 2)])
    robot = BasicRobot(pos=start_pos)

    robot.move(Direction.UP, grid)

    assert robot.pos == start_pos, "Robot shold not move into an obstacle."


def test_sensor() -> None:
    start_pos = Position(1, 1)
    grid = Grid(size=(5, 5), obstacles=[Position(1, 3)])
    sensor_robot = SensorRobot(
        pos=start_pos, sensor=ObstacleSensor(sensor_range=3)
    )

    sensor_readings = sensor_robot.sense_obstacles(grid)

    assert sensor_readings["UP"] == 2
    assert sensor_readings["DOWN"] == 1
    assert sensor_readings["LEFT"] == 1
    assert sensor_readings["RIGHT"] == 3


def test_sensor_varied_obstacles() -> None:
    start_pos = Position(2, 2)
    grid = Grid(
        size=(5, 5),
        obstacles=[
            Position(2, 1),
            Position(4, 2),
            Position(2, 4),
            Position(1, 2),
        ],
    )
    sensor_robot = SensorRobot(
        pos=start_pos, sensor=ObstacleSensor(sensor_range=3)
    )

    sensor_readings = sensor_robot.sense_obstacles(grid)

    assert sensor_readings["UP"] == 2
    assert sensor_readings["DOWN"] == 1
    assert sensor_readings["LEFT"] == 1
    assert sensor_readings["RIGHT"] == 2
