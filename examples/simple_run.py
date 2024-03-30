from examples.constants import CONFIGS_DIR
from robo_sim.algorithms import AlgorithmType
from robo_sim.sim import Sim


def main():
    config_path = CONFIGS_DIR / "sensor_robot.yaml"
    sim = Sim(config_path, AlgorithmType.AStar)
    sim.run()


if __name__ == "__main__":
    main()
