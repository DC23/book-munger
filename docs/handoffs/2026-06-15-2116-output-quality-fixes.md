# Handoff: 2026-06-15-2116 Output quality fixes — issue backlog

## Summary

**Baseline:** 73 tests passing, no uncommitted changes. Epic #1 fully merged (issues #8–#11, #10). Pipeline end-to-end: `book-munger INPUT` → Word Table.
**Outstanding:**
- Issues #27–#32 created and triaged; none yet implemented. See plan `docs/plans/2026-06-15-2116-output-quality-fixes.md`.

---

## What happened

First real-book runs of the full Pipeline against several Project Gutenberg texts (Dracula, At the Mountains of Madness, and others — outputs in `./tables/`). No code was written this session; the session was entirely planning and issue creation.

Five output quality problems were identified and six GitHub issues created. The plan is saved to `docs/plans/2026-06-15-2116-output-quality-fixes.md`.

## Issues created

| Issue | Title | Status |
|---|---|---|
| [#27](https://github.com/DC23/book-munger/issues/27) | Punctuation guard in NLP pipeline | needs-triage |
| [#28](https://github.com/DC23/book-munger/issues/28) | Stopwords infrastructure: spaCy defaults and curated file | needs-triage |
| [#29](https://github.com/DC23/book-munger/issues/29) | Consistent POS column ordering in combined tables | needs-triage |
| [#30](https://github.com/DC23/book-munger/issues/30) | Add POS label reference table to README | needs-triage |
| [#31](https://github.com/DC23/book-munger/issues/31) | Filter chapter heading text from HTML output | needs-triage, blocked by #28 |
| [#32](https://github.com/DC23/book-munger/issues/32) | Blended ranker: union of frequency and distinctiveness outputs | needs-triage, blocked by #27 and #28 |

## Problem summary

**Punctuation in tables (#27):** Tokens like `.`, `!`, `-`, `´` appear in the PROPN and other columns. The `_ALLOWED_POS` filter in `nlp_pipeline.process()` should exclude these, but spaCy mis-tags some punctuation in edge cases. Fix: skip tokens whose lemma contains no alphabetic character.

**Common words (#28):** Running without `--stopwords` gives unfiltered output — common words fill every POS column. Decision: use spaCy's built-in stop words automatically when no `--stopwords` file is given; file overrides. Requires refactoring `filter.py` to separate loading from applying, and updating `cli.py` to resolve Stopwords before calling `apply_stopwords`. Also ship a curated `src/book_munger/data/stopwords-en.txt` as an optional user-facing convenience file (not auto-loaded).

**Column ordering (#29):** Combined Word Table column order varies book to book because `counter.count()` preserves token-encounter order. Fix: define a canonical POS order in `MarkdownWriter` (content words first: PROPN, NOUN, VERB, ADJ, ADV, then function words: PRON, ADP, CCONJ, SCONJ, INTJ) and sort before building the table.

**POS label readability (#30):** Docs-only. Add a reference table to README mapping column headers (`Cconj`, `Sconj`, `Adp`, etc.) to their full part-of-speech names.

**Chapter headings (#31, deferred):** `chapter` appears in some Word Tables. ADR 0004's assumption that it would be suppressed by the wordfreq baseline proved incorrect. Deferred until after #28 lands — if `chapter` is added to the curated stopwords file, the issue may close without code changes. If still needed: strip `<h1>`–`<h6>` in `HtmlReader` before `get_text()`.

**Blended Ranker (#32, deferred):** For some books (notably *At the Mountains of Madness*), a blend of FrequencyRanker and DistinctivenessRanker output would be more evocative than either alone. Proposed approach: take top-N from each, union, deduplicate, sort alphabetically. Defer until #27 and #28 produce cleaner tables to calibrate against.

## Sequencing

#27, #28, #29, #30 are all independent and can be triaged and picked up in any order. #31 and #32 are blocked; do not implement until #28 is done and tables re-run.
