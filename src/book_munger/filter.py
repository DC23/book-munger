from pathlib import Path


def apply_stopwords(
    counts: dict[str, dict[str, int]],
    stopwords_path: Path | None,
) -> dict[str, dict[str, int]]:
    if stopwords_path is None:
        return counts

    stopwords: set[str] = set()
    with open(stopwords_path, encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            if word and not word.startswith("#"):
                stopwords.add(word.lower())

    return {
        pos: {lemma: cnt for lemma, cnt in lemmas.items() if lemma not in stopwords}
        for pos, lemmas in counts.items()
    }
