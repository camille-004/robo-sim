import argparse

from robo_sim import Sim

from .constants import (
    ALGORITHM_EXAMPLES_DIR,
    ENV_EXAMPLES_DIR,
    ROBOT_EXAMPLES_DIR,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="robo_sim", description="Run RoboSim simulations."
    )
    parser.add_argument(
        "env",
        nargs="?",
        default="basic_env",
        help="The environment configuration to use.",
    )
    parser.add_argument(
        "robot", nargs="?", default="basic_robot", help="The robot to use."
    )
    parser.add_argument(
        "algorithm",
        nargs="?",
        default="DWA",
        help="The algorithm to use.",
    )

    args = parser.parse_args()

    if args.env and args.robot and args.algorithm:
        env_config_path = ENV_EXAMPLES_DIR / f"{args.env.lower()}.yaml"
        robot_config_path = ROBOT_EXAMPLES_DIR / f"{args.robot.lower()}.yaml"
        algorithm_config_path = (
            ALGORITHM_EXAMPLES_DIR / f"{args.algorithm.lower()}.yaml"
        )
        sim = Sim(env_config_path, robot_config_path, algorithm_config_path)
        sim.run()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
