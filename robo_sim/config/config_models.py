from pydantic import BaseModel, ConfigDict, Field, validator

from ..utils import Position


class Config(BaseModel):
    steps: int = Field(
        default=20, description="Number of steps for the robot to take."
    )
    env_size: tuple[int, int] = Field(
        default=(10, 10),
        description="Size of the 2D environment as (width, height).",
    )
    start_pos: Position = Field(
        default=Position(1, 1), description="Starting position of the robot."
    )
    target_pos: Position = Field(
        default=Position(8, 8), description="Position of the target."
    )
    obstacles: int | set[Position] = Field(
        default=set(),
        description="List of obstacle positions or number of "
        "obstacles to generate randomly.",
    )
    speed: float = Field(
        default=1.0, description="Distance to move in one step."
    )
    trace_path: bool = Field(
        default=False,
        description="Whether to visually trace the robot's path.",
    )

    @validator("start_pos", "target_pos", pre=True)
    def validate(cls, v):
        if isinstance(v, tuple) and len(v) == 2:
            return Position(*v)
        elif isinstance(v, Position):
            return v
        else:
            raise ValueError("Invalid position format!")

    @validator("obstacles", pre=True)
    def check_obstacles_type(cls, v):
        if isinstance(v, list):
            return set(v)  # List of Positions for coordinates.
        elif isinstance(v, int) or isinstance(v, set):
            return v  # Number of obstacles to generate randomly.
        else:
            raise ValueError(
                "Obstacles must be either a set of coordinates or an integer."
            )

    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)


class SensorConfig(BaseModel):
    sensor_range: int = Field(
        default=3, description="Range of the robot's sensors."
    )


class ProximitySensorConfig(SensorConfig):
    pass


class SensorRobotConfig(Config):
    sensor: SensorConfig = SensorConfig()
