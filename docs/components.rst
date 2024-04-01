How it Works
============

RoboSim is a modular simulation framework. The framework is structured around key components: Grid, Robots, Renderer, and Summarizer.

Grid
****

The Grid component organizes cells into a structured environment, where the robot's movements are simulated. It defines thre boundaries of the simulation space and contains methods to. Obstacles can be explicitly defined in the config or randomly generated, given a number of obstacles.

Cells
-----

There are three types of cells:

* ``EmptyCell``: Represents an unoccupied space that the robot can move through.
* ``ObstacleCell``: Represents an area occupied by an obstacle that the robot cannot pass through. For simplicity, a collision only occurs when the robot's center intersects with the obstacle's center.
* ``TargetCell``: Designates the robot's goal position within the grid.

Cells are identified by their position (``NamedTuple``), making it easy to map the simulation environment's layout and track the robot's location. A cell can be accessed with ``grid[x, y]``.

Robots
******

Robots are the agents navigating through the grid, optionally equipped with sensors to detect obstacles and plan their path towards the target.

Renderer
********

The Renderer visualizes the simulation, showing the robot's movements, sensor range, obstacles, and the target.

* The robot is represented by a circle, with its path optionally traced over time (toggle with ``trace_path`` in your YAML configuration file).
* Obstacles are indicated by black squares, and the target is light green.
* Sensor ranges are visualized differently for continuous (360-degree) sensors and discrete sensors:
    * **Continuous Sensors**: Displays sensor detection lines at various angles around the robot, illustrating a full 360-degree sensory perception.
    * **Discrete Sensors**: Show sensor lines only in four cardinal directions (up, down, left, right), representing a more limited sensory field.

Summarizer
**********

