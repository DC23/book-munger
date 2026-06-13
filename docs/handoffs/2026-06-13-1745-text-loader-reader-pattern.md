# Handoff: 2026-06-13-1745 Text loader — Reader pattern design

## Summary

**Baseline:** 1 test passing (CLI `--help`), clean working tree on branch `3-b-text-loader`
**Outstanding:**
- Issue #3 is `ready-for-agent` — implement per the agent brief and plan

---

## What happened

This session was a planning-first deep dive on issue #3 (Text loader). The original issue spec called for a flat `load(path: Path) -> str` function. After exploring the Project Gutenberg test corpus in `books/pg/` and inspecting the HTML zip format, the design was substantially revised.

### Reader pattern adopted

Issue #3 was redesigned to use a Reader pattern. See [ADR 0005](../adr/0005-reader-pattern-for-input.md) for the full rationale. In brief:

- `BaseReader` abstract class with `read(self) -> str`
- `PlainTextReader` — `.txt`; UTF-8 with latin-1 fallback; strips on PG `*** START/END ***` delimiters
- `HtmlReader` — `.html`/`.htm`/`.zip`; `beautifulsoup4`; removes `id="pg-header"` and `id="pg-footer"` elements
- `reader_for(path)` factory dispatching on file extension
- `process` CLI sub-command wired to `reader_for()`

Key design decisions recorded in the issue body: Readers return plain `str` (structure deferred); boilerplate stripping is each Reader's responsibility; HTML is preferred over plain text for PG sources because the explicit div IDs give sharper content boundaries.

The implementation plan is saved at [docs/plans/2026-06-13-1745-text-loader-reader-pattern.md](../plans/2026-06-13-1745-text-loader-reader-pattern.md).

### Issue #3 triaged to ready-for-agent

An agent brief was posted to [issue #3](https://github.com/DC23/book-munger/issues/3). The brief specifies synthetic test fixtures (not real PG books — copyright status is ambiguous outside the US, and PG re-encodes old files to UTF-8 anyway, making them unreliable for encoding tests).

### Issue #4 closed

The standalone Gutenberg cleaner stage (issue #4) was closed without implementation. The two responsibilities it held are now resolved:

1. PG boilerplate stripping — moved into the Reader classes
2. Chapter heading removal — judged low-value for word frequency tables (sparse, common words suppressed by wordfreq baseline, not universal across texts)

See [ADR 0004](../adr/0004-no-standalone-cleaner-stage.md). The pipeline's composable design means this can be added as a `TextTransformer` stage later if needed.

### ADRs written this session

- [ADR 0004](../adr/0004-no-standalone-cleaner-stage.md) — no standalone cleaner stage
- [ADR 0005](../adr/0005-reader-pattern-for-input.md) — Reader pattern for input

---

## Next session

Implement issue #3 per the agent brief on branch `3-b-text-loader`. The plan at [docs/plans/2026-06-13-1745-text-loader-reader-pattern.md](../plans/2026-06-13-1745-text-loader-reader-pattern.md) has everything needed. Use `/begin-coding` to load context.
