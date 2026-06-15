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

**Status:** promoted
**Source:** docs/handoffs/2026-06-13-2022-counter-filter.md

## Ranker

**Status:** promoted
**Source:** docs/handoffs/2026-06-13-2216-ranker-base-class-and-frequency-ranker.md

## Writer

**Status:** promoted
**Source:** docs/handoffs/2026-06-14-1115-issue-drift-checks-and-triage.md

## Reporter

**Status:** promoted
**Source:** docs/handoffs/2026-06-14-1115-issue-drift-checks-and-triage.md

## Blended Ranker

**Status:** pending
**Source:** docs/handoffs/2026-06-15-2116-output-quality-fixes.md

A Ranker variant that unions the top-N output of FrequencyRanker and DistinctivenessRanker, deduplicates, and sorts alphabetically. Named in issue #32 as a distinct strategy alongside the existing two.
