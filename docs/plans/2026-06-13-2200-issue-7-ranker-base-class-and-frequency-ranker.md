# Plan: Issue #7 — Ranker strategy base class and FrequencyRanker

## Context

Issue #6 (Counter + Filter) is merged. The pipeline now exposes `counter.count()` returning `dict[str, dict[str, int]]` (POS → {lemma: count}) and `filter.apply_stopwords()`. Issue #7 adds the final pipeline stage: a `Ranker` strategy abstraction so the word-selection algorithm is swappable, plus `FrequencyRanker` as the first concrete implementation.

The ranker receives a single POS bucket — `dict[str, int]` — and returns `list[str]` in ranked order. The CLI is responsible for iterating over POS buckets; the ranker is not POS-aware.

## Review findings

The issue spec is solid. Two gaps addressed here:

**Naming**: The issue specifies `class Ranker(ABC)` but the established pattern uses `BaseReader(ABC)`. Using `BaseRanker` to stay consistent.

**`rankers/__init__.py`**: Not mentioned in the issue but required for the package. Empty is sufficient — no factory is warranted with a single implementation.

## Files to create

### `src/book_munger/rankers/__init__.py`

Empty (signals package, no factory yet).

### `src/book_munger/rankers/base.py`

```python
from abc import ABC, abstractmethod


class BaseRanker(ABC):
    @abstractmethod
    def rank(self, counts: dict[str, int], top_n: int) -> list[str]:
        """Given {lemma: count}, return the top_n lemmas in ranked order."""
```

### `src/book_munger/rankers/frequency.py`

```python
from .base import BaseRanker


class FrequencyRanker(BaseRanker):
    def rank(self, counts: dict[str, int], top_n: int) -> list[str]:
        ranked = sorted(counts, key=lambda lemma: counts[lemma], reverse=True)
        return ranked[:top_n]
```

`list[:n]` where `n > len(list)` returns all elements — handles over-large `top_n` without special logic.

## Tests

### `tests/test_frequency_ranker.py`

Four tests (three from acceptance criteria plus one edge case):

1. `test_top_n_returned_in_descending_order` — correct words, correct order
2. `test_ties_broken_consistently` — stable sort on equal counts
3. `test_top_n_larger_than_vocabulary_returns_all` — no error, all words returned
4. `test_empty_counts_returns_empty_list` — not in issue spec, but obvious boundary

## Approach: TDD

Red-green-refactor:
1. Write failing tests, confirm red.
2. Create `rankers/` package with `BaseRanker`.
3. Implement `FrequencyRanker`, confirm green.

## Files not touched

`cli.py`, `counter.py`, `filter.py`, `nlp_pipeline.py` — CLI integration of Ranker is out of scope for this issue.

## Verification

```bash
.venv/bin/pytest tests/test_frequency_ranker.py -v   # four tests green
.venv/bin/pytest --tb=short                           # full suite (37 + 4 = 41) passing
```
