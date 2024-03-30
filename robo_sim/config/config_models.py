from pydantic import BaseModel, Field, validator


class Config(BaseModel):
    steps: int = Field(
        default=20, description="Number of steps for the robot to take."
    )
    grid_size: tuple[int, int] = Field(
        default=(10, 10), description="Size of the 2D grid as (width, height)."
    )
    start_pos: tuple[int, int] = Field(
        default=(1, 1), description="Starting position of the robot."
    )
    target_pos: tuple[int, int] = Field(
        default=(8, 8), description="Position of the target."
    )
    obstacles: int | list[tuple[int, int]] = Field(
        default=[],
        description="List of obstacle positions or number of "
        "obstacles to generate randomly.",
    )
    trace_path: bool = Field(
        default=False, description="Whether to visually trace the robot's path."
    )

    @validator("obstacles", pre=True)
    def check_obstacles_type(cls, v):
        if isinstance(v, list):
            return v  # List of tuples for coordinates.
        elif isinstance(v, int):
            return v  # Number of obstacles to generate randomly.
        else:
            raise ValueError(
                "Obstacles must be either a list of coordinates or an integer."
            )

    class Config:
        extra = "allow"


class SensorRobotConfig(Config):
    sensor_range: int = Field(
        default=3, description="Range of the robot's sensors."
    )
