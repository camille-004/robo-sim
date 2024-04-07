import random

from ..utils import Position


class Cell:
    def __init__(self, pos: Position, color: str = "white") -> None:
        self.pos = pos
        self.color = color

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(pos={self.pos}, color={self.color})"


class EmptyCell(Cell):
    def __init__(self, pos: Position) -> None:
        colors = ["#90EE90", "#98FB98"]
        color = random.choice(colors)
        super().__init__(pos, color=color)


class ObstacleCell(Cell):
    def __init__(self, pos: Position) -> None:
        super().__init__(pos, color="sienna")


class TargetCell(Cell):
    def __init__(self, pos: Position) -> None:
        super().__init__(pos, color="gold")


def create_cell(pos: Position, cell_type: str = "empty", **kwargs) -> Cell:
    match cell_type:
        case "empty":
            return EmptyCell(pos)
        case "obstacle":
            return ObstacleCell(pos, **kwargs)
        case "target":
            return TargetCell(pos, **kwargs)
        case _:
            raise ValueError(f"Unsupported cell type: {cell_type}.")
