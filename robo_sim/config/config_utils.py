from pathlib import Path
from typing import Any

import yaml


def read_yaml_config(config_path: Path) -> Any:
    with config_path.open("r") as f:
        config_data = yaml.safe_load(f)
    return config_data
