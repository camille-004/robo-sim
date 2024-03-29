import logging
from typing import Any

import colorlog


class ColoredFormatter(colorlog.ColoredFormatter):
    def __init__(
        self,
        fmt: Any | None = None,
        datefmt: Any | None = None,
        style: Any | None = "%",
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


def get_logger(name: str | None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter())
    logger.addHandler(console_handler)

    return logger
