import sys
from pathlib import Path

from .config_models import AlgorithmConfig, EnvConfig, RobotConfig
from .config_utils import read_yaml_config


def get_algorithm_config_classes() -> dict[str, type[AlgorithmConfig]]:
    module = sys.modules["robo_sim.config.config_models"]
    return {
        cls.__name__.replace("Config", ""): cls
        for cls in module.__dict__.values()
        if isinstance(cls, type)
        and issubclass(cls, AlgorithmConfig)
        and cls is not AlgorithmConfig
    }


class ConfigFactory:
    def __init__(
        self,
        env_config_path: Path,
        robot_config_path: Path,
        algorithm_config_path: Path,
    ):
        self.env_config_path = env_config_path
        self.robot_config_path = robot_config_path
        self.algorithm_config_path = algorithm_config_path
        self.algorithm_configs = get_algorithm_config_classes()

    def load_env_config(self) -> EnvConfig:
        env_data = read_yaml_config(self.env_config_path)
        return EnvConfig(**env_data)

    def load_robot_config(self) -> RobotConfig:
        robot_data = read_yaml_config(self.robot_config_path)
        return RobotConfig(**robot_data)

    def load_algorithm_config(self) -> AlgorithmConfig:
        algorithm_data = read_yaml_config(self.algorithm_config_path)
        algorithm_type = algorithm_data.get("name", "")
        config_class = self.algorithm_configs.get(
            algorithm_type, AlgorithmConfig
        )
        return config_class(**algorithm_data)
