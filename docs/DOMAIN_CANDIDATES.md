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
