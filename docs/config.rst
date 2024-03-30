Creating a Custom Simulation Config
===================================

When setting up a simulation, a custom configuration allows you to tailor the simulation parameters to your needs. The below model shows the required fields for your basic configuration.

.. autopydantic_model:: robo_sim.config.config_models.Config

If you include sensor options, such as `sensor_range`, your simulation will use a `SensorRobotConfig` subclass.

.. autopydantic_model:: robo_sim.config.config_models.SensorRobotConfig