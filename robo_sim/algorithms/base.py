from abc import ABC, abstractmethod
from typing import Any


class Algorithm(ABC):
    @abstractmethod
    def exec(self, *args: Any, **kwargs: Any) -> None:
        pass
