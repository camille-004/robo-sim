import math
import threading
from typing import TYPE_CHECKING, Any

import matplotlib

matplotlib.use("Qt5Agg")
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.artist import Artist

from ..logging import get_logger
from ..utils import Direction, Position, manhattan_distance
from .grid import Grid
from .robot import ContinuousObstacleSensor

logger = get_logger(__name__)

if TYPE_CHECKING:
    from ..sim import Sim


class Renderer:
    def __init__(
        self,
        grid: Grid,
        trace_path: bool = False,
    ) -> None:
        self.grid = grid
        self.grid_size = grid.size
        self.trace_path = trace_path

        self.sensor_visuals: list[Any] = []
        self.robot_path: list[Position] = []

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
                    color="deepskyblue",
                    alpha=0.3,
                )

    def _draw_discrete_sensors(self, sim: "Sim") -> None:
        if hasattr(sim.robot, "sensor"):
            sensor_readings = sim.robot.sensor.sense(sim.grid, sim.robot.pos)
            for direction, distance in sensor_readings.items():
                dx, dy = Direction[direction].value
                end_pos = sim.robot.pos + (dx * distance, dy * distance)
                (sensor_line,) = self.ax.plot(
                    [sim.robot.pos.x, end_pos.x],
                    [sim.robot.pos.y, end_pos.y],
                    "r--",
                )
                self.sensor_visuals.append(sensor_line)

    def _draw_continuous_sensors(self, sim: "Sim") -> None:
        if hasattr(sim.robot, "sensor"):
            angles = range(0, 360, 5)
            robot_radius = 0.5

            for angle in angles:
                rad = math.radians(angle)
                start_x = sim.robot.pos.x + robot_radius * math.cos(rad)
                start_y = sim.robot.pos.y + robot_radius * math.sin(rad)

                distance = sim.robot.sensor.sense_at_angle(
                    sim.grid, sim.robot.pos, angle
                )

                end_x = sim.robot.pos.x + distance * math.cos(rad)
                end_y = sim.robot.pos.y + distance * math.sin(rad)

                (sensor_line,) = self.ax.plot(
                    [start_x, end_x], [start_y, end_y], "r-", linewidth=0.5
                )
                self.sensor_visuals.append(sensor_line)

    def draw_sensors(self, sim: "Sim") -> None:
        for visual in self.sensor_visuals:
            visual.remove()
        self.sensor_visuals.clear()

        if hasattr(sim.robot, "sensor"):
            if isinstance(sim.robot.sensor, ContinuousObstacleSensor):
                self._draw_continuous_sensors(sim)
            else:
                self._draw_discrete_sensors(sim)

    def draw_grid(self) -> None:
        for cell in self.grid:
            self.ax.add_patch(
                patches.Rectangle(
                    (cell.pos.x - 0.5, cell.pos.y - 0.5),
                    1,
                    1,
                    facecolor=cell.color,
                    edgecolor="none",
                )
            )

        plt.xlabel("X")
        plt.ylabel("Y")

    def update(self, frame: int, sim: "Sim") -> tuple[Artist, ...]:
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

        self.draw_sensors(sim)

        artists = [self.fig]
        artists.extend(self.sensor_visuals)

        if not continue_animation and not self.final_frame:
            self.fig.suptitle(
                f"$\\mathbf{{Frame}}$: {frame + 1}, "
                f"$\\mathbf{{Distance from Target}}$: {distance_to_target}, "
                f"$\\mathbf{{Robot Position}}$: {sim.robot.pos}",
                fontsize=10,
            )
            self.draw_final(sim)
            self.final_frame = True

        return tuple(artists)

    def animate(self, sim: "Sim", steps: int) -> None:
        frames_per_second = 60
        total_frames = frames_per_second * 5

        self.anim = FuncAnimation(
            self.fig,
            self.update,
            fargs=(sim,),
            frames=total_frames,
            repeat=False,
        )
        plt.show()

        close_timer = threading.Timer(5.0, plt.close, args=[self.fig])
        close_timer.start()

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
