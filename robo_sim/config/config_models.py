from pydantic import BaseModel, ConfigDict, Field, validator

from ..utils import Position


class EnvConfig(BaseModel):
    size: tuple[int, int] = Field(
        default=(10, 10),
        description="Size of the 2D environment as (width, height).",
    )
    obstacles: int | set[Position] = Field(
        default=set(),
        description="List of obstacle positions or number of "
        "obstacles to generate randomly.",
    )
    trace_path: bool = Field(
        default=False,
        description="Whether to visually trace the robot's path.",
    )
    max_frames: int = Field(
        default=100,
        description="Maximum frames to reach before the algorithm must be "
        "complete.",
    )
    target_pos: Position = Field(
        default=Position(8, 8), description="Position of the target."
    )

    @validator("target_pos", pre=True)
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
    granularity: int = Field(
        default=5,
        description="Amount of degrees between which to separate sensors.",
    )


class ProximitySensorConfig(SensorConfig):
    pass


class RobotConfig(BaseModel):
    start_pos: Position = Field(
        default=Position(1, 1), description="Starting position of the robot."
    )
    start_orientation: float = Field(
        default=0.0, description="Starting orientation of the robot."
    )
    init_vel: float = Field(
        default=1.0, description="Initial linear velocity."
    )
    init_ang_vel: float = Field(
        default=1.0, description="Initial angular velocity."
    )

    @validator("start_pos", pre=True)
    def validate(cls, v):
        if isinstance(v, tuple) and len(v) == 2:
            return Position(*v)
        elif isinstance(v, Position):
            return v
        else:
            raise ValueError("Invalid position format!")

    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)


class SensorRobotConfig(RobotConfig):
    sensor: SensorConfig = SensorConfig()


class AlgorithmConfig(BaseModel):
    name: str = Field(default="default", description="Name of the algorithm.")


class RRTConfig(AlgorithmConfig):
    max_step_size: float = Field(default=0.5)
    max_iter: int = Field(default=1000)
    goal_sample_rate: int = Field(default=20)
    search_radius: float = Field(default=1.5)
