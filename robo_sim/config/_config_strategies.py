from abc import ABC, abstractmethod

from .config_models import Config, SensorRobotConfig


class ConfigStrategy(ABC):
    @abstractmethod
    def load_config(self, data: dict) -> Config:
        pass


class BasicRobotConfigStrategy(ConfigStrategy):
    def load_config(self, data: dict) -> Config:
        return Config(**data)


class SensorRobotConfigStrategy(ConfigStrategy):
    def load_config(self, data: dict) -> SensorRobotConfig:
        return SensorRobotConfig(**data)
