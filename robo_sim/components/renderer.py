import math
from typing import TYPE_CHECKING

import matplotlib

matplotlib.use("QtAgg")
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.artist import Artist

from ..logging import get_logger
from ..utils import Position, manhattan_distance
from .env import Env
from .sensors import BasicProximitySensor

logger = get_logger(__name__)

if TYPE_CHECKING:
    from ..sim import Sim


class Renderer:
    """RoboSim Renderer class."""

    def __init__(
        self,
        env: Env,
        trace_path: bool = False,
    ) -> None:
        """Constructor for Renderer.

        Parameters
        ----------
        env : Env
            Environment to animate.
        trace_path : bool, optional
            Whether to visually trace the robot's path, by default False
        """
        self.env = env
        self.trace_path = trace_path
        self.robot_path: list[Position] = []
        self.artists: list[Artist] = []
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.setup_plot()

    def setup_plot(self) -> None:
        """Set up the initial plotting parameters."""
        self.ax.set_xlim(0, self.env.size[1])
        self.ax.set_ylim(0, self.env.size[0])
        self.ax.set_aspect("equal")
        self.ax.grid(which="major", color="k", linestyle="--", linewidth=0.5)
        self.ax.set_axisbelow(True)

    def draw_objects(self) -> None:
        for obj in self.env.objects:
            circle = patches.Circle(
                (obj.pos.x, obj.pos.y),
                obj.radius,
                facecolor=obj.color,
                edgecolor="none",
            )
            self.ax.add_patch(circle)
            self.artists.append(circle)

    def draw_robot(self, sim: "Sim") -> None:
        robot_circle = patches.Circle(
            (sim.robot.pos.x, sim.robot.pos.y),
            sim.robot.radius,
            facecolor=sim.robot.color,
            edgecolor="none",
        )
        self.ax.add_patch(robot_circle)
        self.artists.append(robot_circle)

    def update_robot_path(self, robot_pos: Position) -> None:
        if self.trace_path:
            self.robot_path.append(robot_pos)
            path_x = [pos.x for pos in self.robot_path]
            path_y = [pos.y for pos in self.robot_path]
            (path_line,) = self.ax.plot(
                path_x, path_y, color="deepskyblue", linewidth=2, alpha=0.6
            )
            self.artists.append(path_line)

    def draw_sensors(self, sim: "Sim") -> None:
        """Draw sensor beams if the robot has a sensor.

        Parameters
        ----------
        sim : Sim
            Simulation whose animation in which to draw the sensor beams.
        """
        if hasattr(sim.robot, "sensor"):
            if isinstance(sim.robot.sensor, BasicProximitySensor):
                for angle, dist in sim.robot.sensor.sense(
                    sim.env, sim.robot.pos, sim.robot.radius
                ).items():
                    end_x = sim.robot.pos.x + dist * math.cos(
                        math.radians(angle)
                    )
                    end_y = sim.robot.pos.y + dist * math.sin(
                        math.radians(angle)
                    )
                    (sensor_line,) = self.ax.plot(
                        [sim.robot.pos.x, end_x],
                        [sim.robot.pos.y, end_y],
                        "r-",
                        alpha=0.3,
                        linewidth=0.5,
                    )
                    self.artists.append(sensor_line)

    def update(self, frame: int, sim: "Sim", done: bool) -> list[Artist]:
        """Update the visualization each frame based on the simulation
        status."""
        self.ax.clear()
        self.setup_plot()
        self.draw_objects()
        self.update_robot_path(sim.robot.pos)
        self.draw_sensors(sim)
        self.draw_robot(sim)

        distance_to_target = manhattan_distance(sim.robot.pos, sim.target)
        self.fig.suptitle(
            f"$\\mathbf{{Frame}}$: {frame + 1}, "
            f"$\\mathbf{{Distance from Target}}$: {distance_to_target}\n"
            f"$\\mathbf{{Robot Position}}$: {sim.robot.pos}",
            fontsize=10,
        )

        if done:
            completion_text = (
                "Simulation Complete" if sim.reached else "Simulation Ended"
            )
            text = self.ax.text(
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
            self.artists.append(text)

        return self.artists

    def animate_step_by_step(self, sim: "Sim", frame: int, done: bool) -> None:
        self.update(frame, sim, done)
        plt.draw()
        plt.pause(0.1)

    def animate(self, sim: "Sim", steps: int) -> None:
        def update_frame(frame: int) -> list[Artist]:
            return self.update(frame, sim, done=(frame == steps - 1))

        self.anim = FuncAnimation(
            self.fig, update_frame, frames=steps, interval=50, repeat=False
        )
        plt.show()
