# Domain Candidates

## Word Frequency Table

**Status:** rejected — renamed; use Word Table instead. "Frequency" implies frequency is the primary axis of value, which it is not. Word Table is the term in active use.
**Source:** docs/handoffs/2026-06-13-0957-scaffolding.md

## Source Text

**Status:** rejected — too generic; use Book instead. The canonical input is a book; the implementation's generality is not a reason to blur the domain term.
**Source:** docs/handoffs/2026-06-13-0957-scaffolding.md

## Reader

**Status:** promoted
**Source:** docs/handoffs/2026-06-13-1745-text-loader-reader-pattern.md

## Pipeline

**Status:** promoted — defined as the whole Book-to-Word-Table processing chain. The NLP stage is "NLP Pipeline" (`src/book_munger/nlp_pipeline.py`).
**Source:** docs/handoffs/2026-06-13-1820-nlp-pipeline.md

## Stopword

**Status:** pending
**Source:** docs/handoffs/2026-06-13-2022-counter-filter.md

A word excluded from frequency counts before ranking. Loaded from an optional user-supplied file (one word per line, `#` comment lines). Applied after counting, before ranking. Formalised in `src/book_munger/filter.py`.
