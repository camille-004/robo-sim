from abc import ABC, abstractmethod

from ..config import ProximitySensorConfig, SensorConfig
from .sensors import BasicProximitySensor, SensorInterface


class SensorFactory(ABC):
    def __init__(self, config: ProximitySensorConfig) -> None:
        self.config = config

    @abstractmethod
    def create(self) -> SensorInterface:
        raise NotImplementedError("Subclasses must override create().")


class BasicProximitySensorFactory(SensorFactory):
    def create(self) -> BasicProximitySensor:
        return BasicProximitySensor(sensor_range=self.config.sensor_range)


sensor_registry: dict[type[SensorConfig], type[SensorFactory]] = {
    ProximitySensorConfig: BasicProximitySensorFactory,
}


def get_robot(
    config: ProximitySensorConfig,
) -> SensorFactory:  # TODO Change type hint to SensorConfig.
    for config_type, factory in sensor_registry.items():
        if isinstance(config, config_type):
            return factory(config)

    raise ValueError(f"No factory registered for config type {type(config)}.")
