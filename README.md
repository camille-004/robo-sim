# robo-sim

## Getting Started

Ensure that you have the package installed and configured in your environment.
1. Clone the `robo-sim` repository to your machine.
2. Navigate to the root directory of the project.
3. Install the package using `pip`.

```sh
pip install -e .
```

## Running Examples with CLI

RoboSim comes with a set of predefined example configurations located in the `configs` directory. To run an example simulation, use the following CLI command structure.

```sh
robo_sim example <example_name> <algorithm>
```

### Example Command

To run the `sensor_robot` example using the A* algorithm, execute:

```sh
robo_sim example sensor_robot AStar
```

## Running Custom Simulations

1. To create a YAML configuration file for your simulation, refer to for the required structure.
2. Place your YAML file in the `configs` directory.
3. Running your simulation:

### Custom Simulation Command

Assuming your custom configuration file is named `custom_config.yaml`, run:

```sh
robo_sim example my_custom_config AStar
```

### Running the Simulation with Python

```python
from pathlib import Path

from robo_sim.sim import Sim

config_path = Path("my_custom_config.yaml")
sim = Sim(config_path, "AStar")
sim.run()
```
