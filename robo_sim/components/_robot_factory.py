from abc import ABC, abstractmethod

from ..config import Config, SensorRobotConfig
from .robot import BasicRobot, Robot, SensorRobot
from .sensors import BasicProximitySensor


class RobotFactory(ABC):
    def __init__(self, config: Config) -> None:
        self.config = config

    @abstractmethod
    def create(self) -> Robot:
        raise NotImplementedError("Subclasses must override create().")


class BasicRobotFactory(RobotFactory):
    def create(self) -> Robot:
        return BasicRobot(pos=self.config.start_pos)


class SensorRobotFactory(RobotFactory):
    def create(self) -> SensorRobot:
        if not isinstance(self.config, SensorRobotConfig):
            raise ValueError(
                "SensorRobotFactory requires a SensorRobotConfig."
            )

        sensor = BasicProximitySensor(
            sensor_range=self.config.sensor.sensor_range
        )
        return SensorRobot(pos=self.config.start_pos, sensor=sensor)


registry: dict[type[Config], type[RobotFactory]] = {
    SensorRobotConfig: SensorRobotFactory,
    Config: BasicRobotFactory,
}


def get_robot(config: Config) -> RobotFactory:
    for config_type, factory in registry.items():
        if isinstance(config, config_type):
            return factory(config)

    raise ValueError(f"No factory registered for config type {type(config)}.")
