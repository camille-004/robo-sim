import math

from ..utils import Position


class EnvObject:
    def __init__(self, pos: Position) -> None:
        self.pos = pos

    def object_within_range(self, other: "EnvObject") -> bool:
        distance = math.hypot(
            self.pos.x - other.pos.x, self.pos.y - other.pos.y
        )
        return distance <= (self.radius + other.radius)

    def position_within_range(
        self, pos: Position, other_radius: float
    ) -> bool:
        distance = math.hypot(self.pos.x - pos.x, self.pos.y - pos.y)
        return distance <= (self.radius + other_radius)

    @property
    def radius(self) -> float:
        raise NotImplementedError()

    @property
    def color(self) -> str:
        raise NotImplementedError()


class Obstacle(EnvObject):
    def __init__(self, pos: Position) -> None:
        super().__init__(pos)

    @property
    def radius(self):
        return 0.5

    @property
    def color(self):
        return "black"


class Target(EnvObject):
    def __init__(self, pos: Position) -> None:
        super().__init__(pos)

    @property
    def radius(self):
        return 0.5

    @property
    def color(self):
        return "gold"


class EnvObjectFactory:
    @staticmethod
    def create(object_type: str, pos: Position):
        object_registry: dict[str, EnvObject] = {
            "obstacle": Obstacle(pos),
            "target": Target(pos),
        }
        if object_type not in object_registry.keys():
            raise ValueError(f"Unknown object type '{object_type}'.")
        return object_registry[object_type]
