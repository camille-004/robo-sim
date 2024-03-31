from ..utils.types import Position


class Cell:
    def __init__(self, pos: Position) -> None:
        self.pos = pos

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(pos={self.pos})"


class EmptyCell(Cell):
    pass


class ObstacleCell(Cell):
    def __init__(self, pos: Position) -> None:
        super().__init__(pos)


class TargetCell(Cell):
    def __init__(self, pos: Position) -> None:
        super().__init__(pos)


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
