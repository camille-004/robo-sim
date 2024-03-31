from typing import TYPE_CHECKING

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from .grid import CellType, Grid
from .types import Direction, Position
from .utils import manhattan_distance

if TYPE_CHECKING:
    from .sim import Sim


class Renderer:
    def __init__(
        self,
        grid: Grid,
        grid_size: tuple[int, int] = (10, 10),
        trace_path: bool = False,
    ) -> None:
        self.grid = grid
        self.grid_size = grid_size
        self.trace_path = trace_path

        self.sensor_visuals = []
        self.robot_path = []

        self.final_frame = False

        self.fig, self.ax = plt.subplots()
        self.setup_plot()

    def setup_plot(self) -> None:
        self.ax.set_xlim(0, self.grid_size[1])
        self.ax.set_ylim(0, self.grid_size[0])
        self.ax.set_aspect("equal")

        self.ax.set_xticks(range(self.grid_size[1]), minor=True)
        self.ax.set_yticks(range(self.grid_size[0]), minor=True)
        self.ax.grid(which="minor", color="k", linestyle="--", linewidth=0.5)

    def update_robot_path(self, robot_pos: Position) -> None:
        if self.trace_path:
            self.robot_path.append(robot_pos)

    def draw_robot(self, sim: "Sim") -> None:
        robot_circle = patches.Circle(
            sim.robot.pos, 0.3, facecolor="blue", edgecolor="none"
        )
        self.ax.add_patch(robot_circle)

    def draw_robot_path(self) -> None:
        if self.trace_path and len(self.robot_path) > 1:
            for i in range(1, len(self.robot_path)):
                start_pos = self.robot_path[i - 1]
                end_pos = self.robot_path[i]
                self.ax.plot(
                    [start_pos.x, end_pos.x],
                    [start_pos.y, end_pos.y],
                    color="orange",
                    alpha=0.3,
                )

    def draw_sensors(self, sim: "Sim") -> None:
        if not sim.robot.has_sensor_data or not self.visualize_sensors:
            return

        for visual in self.sensor_visuals:
            visual.remove()
        self.sensor_visuals.clear()

        sensor_readings = sim.robot.sense_obstacles(sim.grid)
        for direction, distance in sensor_readings.items():
            dx, dy = Direction[direction].value
            end_pos = Position(
                sim.robot.pos.x + dx * distance,
                sim.robot.pos.y + dy * distance,
            )
            (sensor_line,) = self.ax.plot(
                [sim.robot.pos.x, end_pos.x],
                [sim.robot.pos.y, end_pos.y],
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
        self.update_robot_path(sim.robot.pos)
        self.draw_robot_path()
        self.draw_robot(sim)

        distance_to_target = manhattan_distance(sim.robot.pos, sim.target)

        if continue_animation:
            self.fig.suptitle(
                f"$\\mathbf{{Frame}}$: {frame + 1}, "
                f"$\\mathbf{{Distance from Target}}$: {distance_to_target}, "
                f"$\\mathbf{{Robot Position}}$: {sim.robot.pos}",
                fontsize=10,
            )

        if sim.robot.pos != sim.robot.prev_pos:
            self.visualize_sensors = True
        else:
            self.visualize_sensors = False

        self.draw_sensors(sim)

        if not continue_animation and not self.final_frame:
            self.fig.suptitle(
                f"$\\mathbf{{Frame}}$: {frame + 1}, "
                f"$\\mathbf{{Distance from Target}}$: {distance_to_target}, "
                f"$\\mathbf{{Robot Position}}$: {sim.robot.pos}",
                fontsize=10,
            )
            self.draw_final(sim)
            self.final_frame = True

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
            bbox=dict(
                facecolor="white",
                alpha=0.8,
                edgecolor="gray",
                boxstyle="round,pad=0.5",
            ),
        )
