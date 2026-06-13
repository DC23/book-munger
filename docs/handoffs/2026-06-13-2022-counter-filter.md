# Handoff: 2026-06-13-2022 Word frequency counter and stopword filter

## Summary

**Baseline:** 37 tests passing, clean working tree, branch `6-e-word-frequency-counter-and-stopword-filter` merged to main (commit 3861d66)

---

## What happened

Implemented issue #6 (word frequency counter and stopword filter) in full using TDD. The plan at `docs/plans/2026-06-13-2011-issue-6-counter-filter.md` was followed exactly — no deviations, no architectural decisions required.

### What was built

- `src/book_munger/counter.py` — `count(tokens: Iterable[tuple[str, str]]) -> dict[str, dict[str, int]]`
  - Accumulates `{pos: {lemma: count}}` from Pipeline output using `collections.defaultdict`
  - Returns plain dicts (not defaultdicts) to avoid surprising downstream callers
- `src/book_munger/filter.py` — `apply_stopwords(counts, stopwords_path: Path | None) -> dict[str, dict[str, int]]`
  - `None` path is a strict identity return (same object, not a copy)
  - Stopword file: one word per line, `#`-prefixed lines ignored, blank lines ignored, file entries lower-cased on load
  - Lemma matching is exact (pipeline already lowercases all lemmas, so no `.lower()` needed at match time)
- `tests/test_counter.py` — 8 tests
- `tests/test_filter.py` — 9 tests

### TDD notes

Both modules followed clean red-green cycles with no mid-cycle corrections. The `test_none_path_is_identity_not_copy` test explicitly asserts `result is sample_counts` — this documents a deliberate design choice (avoid unnecessary allocation for the common no-filter case) and guards against future refactoring that inadvertently copies.

### Artefacts

- Plan: `docs/plans/2026-06-13-2011-issue-6-counter-filter.md`
- Implementation commit: 98d432e
- Merge commit: 3861d66 (PR #19)

## Next

Issue #7 (FrequencyRanker) is the next item in the epic — it consumes `counter.count()` output directly. No blockers remain.
