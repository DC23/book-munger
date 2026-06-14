# Handoff: 2026-06-14-1451 Issue #11 DistinctivenessRanker

## Summary

**Baseline:** 46 tests passing (up from 41; 5 new tests for DistinctivenessRanker)
**Outstanding:**
- Branch `11-j-distinctivenessranker-wordfreq-based` is 2 commits ahead of origin — not yet pushed

---

## What happened

Issue #11 implemented end-to-end using TDD. The session also amended the #10 plan after a discussion about where `ranker_for()` dispatch belongs.

---

## Implementation

`DistinctivenessRanker` is in `src/book_munger/rankers/distinctive.py`. Algorithm per ADR 0003 and `docs/plans/2026-06-14-0001-issue-11-distinctiveness-ranker.md`:

```
score = corpus_count / zipf_frequency(lemma, "en")
```

Unknown words (zipf = 0.0) receive `float("inf")` and rank maximally. Sorted descending, sliced to `top_n`. Mirrors `FrequencyRanker` in structure.

Tests in `tests/test_distinctive_ranker.py` (5 tests, all using `unittest.mock.patch` for controlled `zipf_frequency` values where precision matters):

1. Empty input returns `[]`
2. `top_n` larger than vocabulary returns all lemmas
3. Rare word outranks common word at equal corpus count
4. Unknown word (zipf = 0.0) ranks first without error
5. Ties broken consistently across calls (stable sort)

Commits:
- `6f0b019` — Implement DistinctivenessRanker (issue #11)
- `1f81f51` — Plan #10: flag ranker_for() dispatch as a spec gap

---

## Plan #10 amendment

A discussion about whether `rankers/__init__.py` re-exports were worth adding now surfaced a gap in the #10 plan: the `--ranker TEXT` option was specified but the string→class dispatch mechanism was not. Added a "Spec gap flagged for agent" section to `docs/plans/2026-06-14-0003-issue-10-cli-interface.md` pointing at `ranker_for(name: str) -> BaseRanker` as the pattern, following `reader_for()` in `src/book_munger/readers/__init__.py`.

No re-exports were added to `rankers/__init__.py` — the factory is the right shape, and it belongs in the #10 session.

---

## Next sessions

Remaining open issues in order:

1. **#9** (BaseWriter + MarkdownWriter) — parallelisable with #8; plan at `docs/plans/2026-06-14-0002-issue-9-markdown-writer.md`
2. **#8** (HTML ranker report) — was blocked by #11, now unblocked; plan at `docs/plans/2026-06-14-0000-issue-8-html-ranker-report.md`
3. **#10** (CLI) — goes last; plan at `docs/plans/2026-06-14-0003-issue-10-cli-interface.md`
