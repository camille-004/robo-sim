import logging
from pathlib import Path
from typing import Any, Literal

import colorlog

StyleType = Literal["%", "{", "$"]


class ColoredFormatter(colorlog.ColoredFormatter):
    def __init__(
        self,
        fmt: Any | None = None,
        datefmt: Any | None = None,
        style: StyleType = "%",
    ) -> None:
        super().__init__(
            fmt=fmt or "%(log_color)s%(asctime)s - %(name)s | %(message)s",
            datefmt=datefmt,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
            style=style,
        )


def get_logger(
    name: str | None, log_file: Path = Path("sim.txt")
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColoredFormatter())
        logger.addHandler(console_handler)

        file_handler = logging.FileHandler(log_file, mode="a")
        file_format = "%(asctime)s - %(name)s | %(levelname)s | %(message)s"
        file_handler.setFormatter(logging.Formatter(file_format))
        logger.addHandler(file_handler)

    return logger
