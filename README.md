# Getting Started

Ensure that you have the package installed and configured in your environment.
1. Clone the [`robo-sim`](https://github.com/camille-004/robo-sim/tree/main) repository to your machine.
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

1. To create a YAML configuration file for your simulation, refer to the `Config` model descriptions in the documentation for the required structure.
2. Run your simulation with the below script. To see the the rest of supported algorithms, refer to [`robo_sim/algorithms/enums.py`](https://github.com/camille-004/robo-sim/blob/main/robo_sim/algorithms/enums.py).

```python
from pathlib import Path

from robo_sim import Sim

config_path = Path("my_custom_config.yaml")
sim = Sim(config_path, algorithm="AStar")
sim.run()
```
