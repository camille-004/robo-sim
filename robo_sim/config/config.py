from pydantic import BaseModel, Field


class SimConfig(BaseModel):
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
    obstacles: list[tuple[int, int]] = Field(
        default=[], description="List of obstacle positions."
    )

    class Config:
        populate_by_name = True
