# Domain Candidates

## Word Frequency Table

**Status:** pending
**Source:** docs/handoffs/2026-06-13-0957-scaffolding.md

The core output artefact of the tool — a table of words drawn from a source text, annotated with frequency or rank data, shaped by a thematic filter. Appears in the project description and in the epic. The exact shape (columns, ranking method, thematic criteria) is not yet defined.

## Source Text

**Status:** pending
**Source:** docs/handoffs/2026-06-13-0957-scaffolding.md

An input document (book or similar long-form text) that the tool processes to produce word frequency tables. Distinguishes the project's domain input from generic "files" or "data".

## Reader

**Status:** pending
**Source:** docs/handoffs/2026-06-13-1745-text-loader-reader-pattern.md

A pipeline component that loads a Source Text from disk and returns cleaned body text as a plain string. Format-specific boilerplate removal is the Reader's responsibility. Introduced in ADR 0005.

## Pipeline

**Status:** pending
**Source:** docs/handoffs/2026-06-13-1820-nlp-pipeline.md

The NLP processing stage that receives body text from a Reader and yields (lemma, pos) pairs for downstream frequency counting. Implemented in `src/book_munger/pipeline.py`. Distinct from the broader word-processing pipeline (Reader → Pipeline → ...) of which it is one stage.

## Stopword

**Status:** pending
**Source:** docs/handoffs/2026-06-13-2022-counter-filter.md

A word excluded from frequency counts before ranking. Loaded from an optional user-supplied file (one word per line, `#` comment lines). Applied after counting, before ranking. Formalised in `src/book_munger/filter.py`.
