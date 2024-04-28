from pathlib import Path

CURRENT_DIR = Path(__file__).parent.parent.absolute()
EXAMPLES_DIR = CURRENT_DIR.parent / "examples"
ENV_EXAMPLES_DIR = EXAMPLES_DIR / "envs"
ALGORITHM_EXAMPLES_DIR = EXAMPLES_DIR / "algorithms"
ROBOT_EXAMPLES_DIR = EXAMPLES_DIR / "robots"
