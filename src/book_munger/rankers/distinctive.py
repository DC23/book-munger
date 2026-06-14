from wordfreq import zipf_frequency

from .base import BaseRanker


class DistinctivenessRanker(BaseRanker):
    def rank(self, counts: dict[str, int], top_n: int) -> list[str]:
        def score(lemma):
            zipf = zipf_frequency(lemma, "en")
            return counts[lemma] / zipf if zipf > 0 else float("inf")

        ranked = sorted(counts, key=score, reverse=True)
        return ranked[:top_n]
