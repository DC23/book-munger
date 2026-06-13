from abc import ABC, abstractmethod
from pathlib import Path


class BaseReader(ABC):
    def __init__(self, path: Path) -> None:
        self.path = path

    @abstractmethod
    def read(self) -> str:
        """Return cleaned book text as a plain string with boilerplate removed."""
