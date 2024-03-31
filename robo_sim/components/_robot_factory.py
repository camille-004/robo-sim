from abc import ABC, abstractmethod

from ..config import Config, SensorRobotConfig
from .robot import Robot, SensorRobot


class RobotFactory(ABC):
    @abstractmethod
    def create_robot(self, config: Config) -> Robot:
        raise NotImplementedError("Subclasses must override create_robot().")


class BasicRobotFactory(RobotFactory):
    def create_robot(self, config: Config) -> Robot:
        return Robot(pos=config.start_pos)


class SensorRobotFactory(RobotFactory):
    def create_robot(self, config: SensorRobotConfig) -> SensorRobot:
        return SensorRobot(
            pos=config.start_pos, sensor_range=config.sensor_range
        )


registry: dict[Config, RobotFactory] = {
    Config: BasicRobotFactory(),
    SensorRobotConfig: SensorRobotFactory(),
}
