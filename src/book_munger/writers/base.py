from abc import ABC, abstractmethod
from pathlib import Path


class BaseWriter(ABC):
    @abstractmethod
    def write(self, ranked: dict[str, list[str]], path: Path, split: bool = False) -> None:
        """Write ranked word lists. split=False: combined file; split=True: one file per POS."""
        raise NotImplementedError
