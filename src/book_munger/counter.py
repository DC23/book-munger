from collections import defaultdict
from typing import Iterable


def count(tokens: Iterable[tuple[str, str]]) -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for lemma, pos in tokens:
        result[pos][lemma] += 1
    return {pos: dict(lemmas) for pos, lemmas in result.items()}
