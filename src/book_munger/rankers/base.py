from abc import ABC, abstractmethod


class BaseRanker(ABC):
    @abstractmethod
    def rank(self, counts: dict[str, int], top_n: int) -> list[str]:
        """Given {lemma: count}, return the top_n lemmas in ranked order."""
