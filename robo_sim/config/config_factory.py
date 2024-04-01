from pathlib import Path

from .config_models import Config, SensorRobotConfig
from .config_utils import read_yaml_config


class ConfigFactory:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.data = read_yaml_config(config_path)
        self.configs = {
            "sensor": SensorRobotConfig,
            "default": Config,
        }

    def load(self) -> Config:
        for key, config in self.configs.items():
            if key in self.data:
                return config(**self.data)
        return self.configs["default"](**self.data)
