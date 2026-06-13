# 0004: No standalone cleaner stage in the text processing pipeline

**Status:** Accepted

## Context

The original pipeline design included a dedicated `cleaner` module after the text loader, responsible for two things:

1. Stripping Project Gutenberg preamble and postamble (the `*** START/END OF THE PROJECT GUTENBERG EBOOK ***` delimiters and everything outside them)
2. Removing chapter and part headings (lines matching patterns like `CHAPTER I`, `Part Two`, etc.)

During the design of the Reader pattern (issue #3), the pipeline architecture was revised. Readers became responsible for extracting clean body text from their respective formats, with format-specific boilerplate removal handled internally.

## Decision

No standalone cleaner stage. The pipeline goes directly from Reader output to downstream processing.

**Preamble/postamble stripping** is now the Reader's responsibility. `PlainTextReader` slices on the PG delimiter markers; `HtmlReader` removes the `id="pg-header"` and `id="pg-footer"` elements. This binding is deliberate — the most effective stripping method is format-specific, and a format-agnostic text pass would either duplicate the logic or be weaker.

**Chapter heading removal** is not worth a pipeline stage for this use case:

- Chapter headings are sparse relative to body text; they contribute negligible signal to word frequency tables.
- Common words in headings (`chapter`, `part`) are suppressed by the general-language frequency baseline (wordfreq) regardless.
- Numeric and roman numeral tokens (`I`, `II`, `IV`, `1`) appear in body text too and are not distinctively heading-like.
- Chapter headings are not universal — many PG texts use other structural conventions, making a regex-based approach fragile.

## Consequences

- Issue #4 (Gutenberg cleaner) is closed without implementation.
- If a future use case requires heading removal (e.g. structural analysis, section-level frequency tables), a `TextTransformer` stage can be added to the pipeline. The Reader pattern's clean `str` output makes this composable without touching the Reader implementations.
- Any text passed downstream from a Reader is assumed to be boilerplate-free body content.
