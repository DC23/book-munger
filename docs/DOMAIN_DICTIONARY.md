# Domain Dictionary

## Book

A long-form written work — primarily out-of-copyright, public domain, or Creative Commons licensed — that serves as the input to book-munger. The tool is designed around books as the canonical input, though the implementation accepts any plain text or HTML document.

## Pipeline

The end-to-end processing chain that transforms a Book into a Word Table: Reader → NLP Pipeline → Counter → Filter → Ranker. "Pipeline" without qualification always refers to the whole chain.

**Why this name:** "NLP Pipeline" names the specific spaCy lemmatisation stage (`src/book_munger/nlp_pipeline.py`); "Pipeline" alone is reserved for the full chain to avoid ambiguity.

## Reader

A pipeline component that loads a Book from disk and returns cleaned body text as a plain string. Format-specific boilerplate removal is the Reader's responsibility.

**Relationships:** Introduced in ADR 0005. Concrete implementations include `PlainTextReader` and `HtmlReader`; `reader_for()` selects the appropriate Reader for a given file.

## Word Table

The core output artefact of book-munger — a curated list of words drawn from a Source Text, selected and ranked for thematic creative use. Analogous to Mythic Meaning Tables and spark tables (Electric Bastionland). The ranking method is not fixed: frequency, distinctiveness, and other criteria are all valid axes depending on the Ranker used.
