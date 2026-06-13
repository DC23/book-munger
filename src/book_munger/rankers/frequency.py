from .base import BaseRanker


class FrequencyRanker(BaseRanker):
    def rank(self, counts: dict[str, int], top_n: int) -> list[str]:
        ranked = sorted(counts, key=lambda lemma: counts[lemma], reverse=True)
        return ranked[:top_n]
