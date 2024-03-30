import argparse

from robo_sim.sim import Sim

from .constants import EXAMPLES_DIR


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="robo_sim", description="Run RoboSim simulations."
    )
    parser.add_argument(
        "example", nargs="?", default="example", help="The example to run."
    )
    parser.add_argument(
        "simulation",
        nargs="?",
        help="The simulation to run, e.g., 'sensor_robot'.",
    )
    parser.add_argument(
        "algorithm", nargs="?", help="The algorithm to run, e.g., 'astar'."
    )

    args = parser.parse_args()

    if args.example == "example" and args.simulation and args.algorithm:
        config_path = EXAMPLES_DIR / f"{args.simulation}.yaml"
        sim = Sim(config_path, args.algorithm)
        sim.run()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
