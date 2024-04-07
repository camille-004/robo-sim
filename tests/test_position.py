import pytest

from robo_sim.utils import Position


@pytest.mark.parametrize(
    "base, other, expected",
    [
        (Position(2, 3), (1, -1), Position(3, 2)),
        (Position(0, 0), Position(-1, -2), Position(-1, -2)),
        (Position(5, 5), (-3, -3), Position(2, 2)),
    ],
)
def test_position_addition(
    base: Position, other: tuple[int, int] | Position, expected: Position
) -> None:
    assert base + other == expected


@pytest.mark.parametrize(
    "base, other, expected",
    [
        (Position(2, 3), (1, 1), Position(1, 2)),
        (Position(0, 0), Position(1, 2), Position(-1, -2)),
        (Position(5, 5), (3, 3), Position(2, 2)),
    ],
)
def test_position_subtraction(
    base: Position, other: tuple[int, int] | Position, expected: Position
) -> None:
    assert base - other == expected
