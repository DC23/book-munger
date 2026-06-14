# Plan: DistinctivenessRanker (issue #11)

## Context

Issue #11 was written early in the project. Two drift points found against the current codebase:

1. The AC references `DistinctivenessRanker(Ranker)` — the actual base class is `BaseRanker`.
2. The verification section assumes `--ranker` CLI flags that do not exist; the CLI currently has only a `process` command.

Everything else (algorithm, dependency, file path, test scenarios) is still accurate.

## Algorithm

```
distinctiveness_score = corpus_count / zipf_frequency(lemma, "en")
```

- `corpus_count` — raw count from the Counter/Filter stage
- `zipf_frequency(lemma, "en")` — from `wordfreq`; returns `0.0` for unknown words
- Unknown words (zipf = 0.0) are treated as maximally distinctive — use `float("inf")` as their score
- Rank descending by score; slice `[:top_n]`

Documented in ADR 0003 (`docs/adr/0003-retain-wordfreq.md`).

## Files to create

```
src/book_munger/rankers/distinctive.py     (DistinctivenessRanker)
tests/test_distinctive_ranker.py
```

Pattern: mirror `FrequencyRanker` (`src/book_munger/rankers/frequency.py`) and its tests (`tests/test_frequency_ranker.py`).

## Implementation sketch

```python
from wordfreq import zipf_frequency
from .base import BaseRanker


class DistinctivenessRanker(BaseRanker):
    def rank(self, counts: dict[str, int], top_n: int) -> list[str]:
        def score(lemma):
            zipf = zipf_frequency(lemma, "en")
            return counts[lemma] / zipf if zipf > 0 else float("inf")

        ranked = sorted(counts, key=score, reverse=True)
        return ranked[:top_n]
```

## Tests (TDD)

`tests/test_distinctive_ranker.py`:

1. A rare but repeated word ranks above a common word with the same count
2. Unknown words (zipf = 0.0) are handled without error and ranked maximally high
3. Empty input returns `[]`
4. Over-large `top_n` returns all lemmas (consistent with FrequencyRanker)
5. Ties in distinctiveness score are broken consistently (stable sort)

Use synthetic `counts` dicts — no real books. For test 1, wordfreq can be called directly with known rare/common words, or mock `zipf_frequency` to avoid network/corpus dependency concerns.

## Verification

```bash
pytest tests/test_distinctive_ranker.py -v
pytest  # full suite, confirm no regressions
```
