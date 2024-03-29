from examples.constants import CONFIGS_DIR
from robo_sim.config import SimConfig, read_yaml_config
from robo_sim.sim import Sim


def main():
    config_data = read_yaml_config(CONFIGS_DIR / "example.yaml")
    config = SimConfig(**config_data)
    simulation = Sim(config=config)
    simulation.run()


if __name__ == "__main__":
    main()
