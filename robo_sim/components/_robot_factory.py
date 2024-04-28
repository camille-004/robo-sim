from abc import ABC, abstractmethod

from ..config import RobotConfig, SensorRobotConfig
from .robot import BasicRobot, Robot, SensorRobot
from .sensors import BasicProximitySensor


class RobotFactory(ABC):
    def __init__(self, config: RobotConfig) -> None:
        self.config = config

    @abstractmethod
    def create(self) -> Robot:
        raise NotImplementedError("Subclasses must override create().")


class BasicRobotFactory(RobotFactory):
    def create(self) -> Robot:
        return BasicRobot(
            pos=self.config.start_pos,
            init_vel=self.config.init_vel,
            init_ang_vel=self.config.init_ang_vel,
            orientation=self.config.start_orientation,
        )


class SensorRobotFactory(RobotFactory):
    def create(self) -> SensorRobot:
        if not isinstance(self.config, SensorRobotConfig):
            raise ValueError(
                "SensorRobotFactory requires a SensorRobotConfig."
            )

        sensor = BasicProximitySensor(
            sensor_range=self.config.sensor.sensor_range,
            granularity=self.config.sensor.granularity,
        )
        return SensorRobot(
            pos=self.config.start_pos,
            init_vel=self.config.init_vel,
            init_ang_vel=self.config.init_ang_vel,
            orientation=self.config.start_orientation,
            sensor=sensor,
        )


registry: dict[type[RobotConfig], type[RobotFactory]] = {
    SensorRobotConfig: SensorRobotFactory,
    RobotConfig: BasicRobotFactory,
}


def get_robot(config: RobotConfig) -> RobotFactory:
    for config_type, factory in registry.items():
        if isinstance(config, config_type):
            return factory(config)

    raise ValueError(f"No factory registered for config type {type(config)}.")
