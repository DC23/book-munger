# Plan: Issue #6 — Word frequency counter and stopword filter

## Context

Issue #5 (NLP pipeline) is merged. The pipeline exposes `process(text, model) -> Iterable[tuple[str, str]]` where each tuple is `(lemma, pos_tag)` with lemma already lowercased. Issue #6 is the next step: accumulate those tuples into POS-keyed frequency counts, then optionally strip stopwords. This unblocks issue #7 (FrequencyRanker).

The issue specifies exact signatures and acceptance criteria — no design decisions needed.

## Files to create

### `counter.py` in the `book_munger` package

```python
from collections import defaultdict
from typing import Iterable


def count(tokens: Iterable[tuple[str, str]]) -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for lemma, pos in tokens:
        result[pos][lemma] += 1
    return {pos: dict(lemmas) for pos, lemmas in result.items()}
```

### `filter.py` in the `book_munger` package

```python
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
```

Note: `lemma not in stopwords` without `.lower()` because the pipeline already lowercases all lemmas. Case-insensitive handling applies only to stopword file entries on load.

## Tests

### `test_counter.py`

Synthetic fixture embedded in the test file. Cover:
- Correct per-POS bucket structure from a known token list
- Counts accumulate correctly for repeated lemmas
- Multiple POS tags produce separate buckets
- Empty input returns empty dict

### `test_filter.py`

Use `pytest`'s `tmp_path` for the stopword file. Cover:
- `None` path returns counts unchanged (identity)
- Matching lemmas removed from all POS buckets
- Non-matching lemmas preserved
- `#` comment lines in stopword file ignored
- Blank lines ignored
- Uppercase entries in stopword file still match (case-insensitive load)

## Approach: TDD

Red-green-refactor:
1. Write failing tests for `counter.py`, run pytest to confirm red.
2. Implement `counter.py`, confirm green.
3. Write failing tests for `filter.py`, confirm red.
4. Implement `filter.py`, confirm green.

## Reuse

- NLP pipeline's `process()` output format `(lemma, pos)` is the counter's input — no changes to pipeline needed.
- No new dependencies required.

## Verification

```bash
.venv/bin/pytest tests/test_counter.py tests/test_filter.py -v
.venv/bin/pytest --tb=short   # full suite regression check
```
