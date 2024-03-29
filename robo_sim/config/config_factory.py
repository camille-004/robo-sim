from pathlib import Path

from .config_models import Config
from .config_strategies import (
    BasicRobotConfigStrategy,
    SensorRobotConfigStrategy,
)
from .config_utils import read_yaml_config


class ConfigFactory:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.strategies = {
            "sensor_range": SensorRobotConfigStrategy(),
            "default": BasicRobotConfigStrategy(),
        }

    def load(self) -> Config:
        data = read_yaml_config(self.config_path)
        for key, strategy in self.strategies.items():
            if key in data:
                return strategy.load_config(data)
        return self.strategies["default"].load_config(data)
