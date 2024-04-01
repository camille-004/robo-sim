from abc import ABC, abstractmethod

from ..config import Config, SensorRobotConfig
from .robot import ContinuousSensorRobot, Robot, SensorRobot


class RobotFactory(ABC):
    def __init__(self, config: Config) -> None:
        self.config = config

    @abstractmethod
    def create(self) -> Robot:
        raise NotImplementedError("Subclasses must override create_robot().")


class BasicRobotFactory(RobotFactory):
    def create(self) -> Robot:
        return Robot(pos=self.config.start_pos)


class SensorRobotFactory(RobotFactory):
    def create(self) -> SensorRobot:
        if self.config.sensor.continuous:
            return ContinuousSensorRobot(
                pos=self.config.start_pos,
                sensor_range=self.config.sensor.sensor_range,
            )
        else:
            return SensorRobot(
                pos=self.config.start_pos,
                sensor_range=self.config.sensor.sensor_range,
            )


registry: dict[Config, RobotFactory] = {
    SensorRobotConfig: SensorRobotFactory,
    Config: BasicRobotFactory,
}


def get_robot(config: Config) -> RobotFactory:
    for config_type, factory in registry.items():
        if isinstance(config, config_type):
            return factory(config)

    raise ValueError(f"No factory registered for config type {type(config)}.")
