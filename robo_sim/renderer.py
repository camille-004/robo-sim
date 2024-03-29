from typing import TYPE_CHECKING

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from .grid import CellType, Grid
from .robot import Direction

if TYPE_CHECKING:
    from .sim import Sim


class Renderer:
    def __init__(
        self, grid: Grid, grid_size: tuple[int, int] = (10, 10)
    ) -> None:
        self.grid = grid
        self.grid_size = grid_size
        self.fig, self.ax = plt.subplots()
        self.sensor_visuals = []

        self.ax.set_xlim(0, self.grid_size[1])
        self.ax.set_ylim(0, self.grid_size[0])
        self.ax.set_aspect("equal")

        self.ax.set_xticks(range(self.grid_size[1]), minor=True)
        self.ax.set_yticks(range(self.grid_size[0]), minor=True)
        self.ax.grid(which="minor", color="k", linestyle="--", linewidth=0.5)

        self.final_frame = False

    def draw_sensors(self, sim: "Sim") -> None:
        for visual in self.sensor_visuals:
            visual.remove()
        self.sensor_visuals.clear()

        if sim.robot.has_sensor_data:
            sensor_readings = sim.robot.sense_obstacles(sim.grid)
            for direction, distance in sensor_readings.items():
                dx, dy = Direction[direction].value
                end_pos = (
                    sim.robot.pos[0] + dx * distance,
                    sim.robot.pos[1] + dy * distance,
                )
                (sensor_line,) = self.ax.plot(
                    [sim.robot.pos[0], end_pos[0]],
                    [sim.robot.pos[1], end_pos[1]],
                    "r--",
                )
                self.sensor_visuals.append(sensor_line)

    def draw_grid(self) -> None:
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                color = "white"
                match self.grid.grid[x, y]:
                    case CellType.OBSTACLE:
                        color = "black"
                    case CellType.ROBOT:
                        color = "blue"
                    case CellType.TARGET:
                        color = "red"

                self.ax.add_patch(
                    patches.Rectangle(
                        (x - 0.5, y - 0.5),
                        1,
                        1,
                        facecolor=color,
                        edgecolor="none",
                    )
                )

        plt.xlabel("X")
        plt.ylabel("Y")

    def update(self, frame: int, sim: "Sim") -> None:
        continue_animation = sim.update()
        self.draw_grid()

        if not continue_animation and not self.final_frame:
            self.draw_final(sim)
            self.final_frame = True

        self.draw_sensors(sim)

    def animate(self, sim: "Sim", steps: int) -> None:
        self.anim = FuncAnimation(
            self.fig, self.update, fargs=(sim,), frames=steps, repeat=False
        )
        plt.show()

    def draw_final(self, sim: "Sim") -> None:
        completion_text = (
            "Simulation Complete" if sim.reached else "Simulation Ended"
        )
        self.ax.text(
            0.5,
            0.5,
            completion_text,
            transform=self.ax.transAxes,
            ha="center",
            fontsize=14,
            color="green",
        )
