from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..utils import Position


class Config(BaseModel):
    steps: int = Field(
        default=20, description="Number of steps for the robot to take."
    )
    grid_size: tuple[int, int] = Field(
        default=(10, 10), description="Size of the 2D grid as (width, height)."
    )
    start_pos: Position = Field(
        default=(1, 1), description="Starting position of the robot."
    )
    target_pos: Position = Field(
        default=(8, 8), description="Position of the target."
    )
    obstacles: int | list[Position] = Field(
        default=[],
        description="List of obstacle positions or number of "
        "obstacles to generate randomly.",
    )
    trace_path: bool = Field(
        default=False,
        description="Whether to visually trace the robot's path.",
    )

    @field_validator("start_pos", "target_pos")
    def validate(cls, v):
        if isinstance(v, tuple) and len(v) == 2:
            return Position(*v)
        elif isinstance(v, Position):
            return v
        else:
            raise ValueError("Invalid position format!")

    @field_validator("obstacles")
    def check_obstacles_type(cls, v):
        if isinstance(v, list):
            return v  # List of Positions for coordinates.
        elif isinstance(v, int):
            return v  # Number of obstacles to generate randomly.
        else:
            raise ValueError(
                "Obstacles must be either a list of coordinates or an integer."
            )

    model_config = ConfigDict(extra="allow")


class SensorConfig(BaseModel):
    sensor_range: int = Field(
        default=3, description="Range of the robot's sensors."
    )
    continuous: bool = Field(
        default=False,
        description="Whether the robot uses continuous sensor scanning.",
    )


class SensorRobotConfig(Config):
    sensor: SensorConfig = SensorConfig()
