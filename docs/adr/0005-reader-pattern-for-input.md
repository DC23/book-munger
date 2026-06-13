# 0005: Reader pattern for text input

**Status:** Accepted

## Context

Issue #3 (Text loader) originally specified a flat `load(path: Path) -> str` function in a single module. During planning, two factors pushed toward a more structured design: the availability of both plain text and zipped HTML formats for Project Gutenberg books, and the recognition that boilerplate stripping (which differs significantly between formats) belonged alongside the format-specific parsing logic rather than in a separate stage.

## Decision

Use a Reader pattern on the input side of the pipeline:

- `BaseReader` — abstract class with a single `read(self) -> str` method
- `PlainTextReader` — handles `.txt`; encoding fallback (UTF-8 → latin-1); strips PG preamble/postamble on `*** START/END OF THE PROJECT GUTENBERG EBOOK ***` delimiters
- `HtmlReader` — handles `.html`, `.htm`, and `.zip` (PG-format zipped HTML); parses with `beautifulsoup4`; removes `id="pg-header"` and `id="pg-footer"` elements
- `reader_for(path: Path) -> BaseReader` — factory dispatching on file extension

Boilerplate stripping is bound to each concrete Reader, not extracted into a separate stage. The rationale: stripping quality is format-specific (HTML's explicit `id` attributes give sharper boundaries than regex on delimiter lines), and a format-agnostic pass would either duplicate logic or produce weaker results.

All Readers return a plain `str`. Structured output (paragraphs, chapters) is deferred until a concrete downstream need arises.

## Consequences

- `beautifulsoup4` is added as a runtime dependency.
- The pipeline extension point for new input formats is `BaseReader` — add a subclass and a branch in `reader_for()`.
- Text passed downstream from any Reader is treated as boilerplate-free body content.
- This decision supersedes the original flat `load()` function design for issue #3.
- See also ADR 0004: the Reader pattern's format-specific boilerplate handling was one of two reasons the standalone cleaner stage (issue #4) was closed without implementation.
