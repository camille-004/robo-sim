from pathlib import Path
from typing import Any

import yaml


def construct_tuple(loader: yaml.Loader, node: yaml.SequenceNode) -> tuple:
    return tuple(loader.construct_sequence(node))


yaml.Loader.add_constructor("tag:yaml.org,2002:python/tuple", construct_tuple)


def read_yaml_config(config_path: Path) -> Any:
    with config_path.open("r") as f:
        config_data = yaml.load(f, Loader=yaml.Loader)
    return config_data
