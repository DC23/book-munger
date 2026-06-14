# Plan: CLI interface (issue #10)

## Context

Issue #10 was written before several design decisions were finalised:
- The CLI shape (subcommands vs single command) was unspecified
- The default ranker was set to `frequency`; the user has since confirmed `distinctive` is the intended default
- Combined output (all POS in one file) is now the default mode, not split
- The HTML report was treated as always-generated pipeline output; it is now an opt-in flag

All components (#8 HTML reporter, #9 writer, #11 DistinctivenessRanker) will be implemented before #10.

## Revised CLI surface

```
book-munger INPUT [OPTIONS]

  INPUT              Source text file (format auto-detected by reader_for())

Options:
  --output PATH      Output directory or file path [default: current dir]
  --output-name NAME Override output filename root [default: input file stem]
  --stopwords PATH   Stopword list file; no filtering if omitted
  --top-n INT        Words per POS list [default: 100]
  --pos TEXT         Comma-separated POS filter e.g. noun,adjective [default: all]
  --ranker TEXT      Ranking strategy: frequency | distinctive [default: distinctive]
  --split            Write one file per POS instead of combined [default: combined]
  --html-report      Also generate HTML ranker report [default: off]
```

`cli.py` becomes a `@click.command()` (not a group). The existing `process` subcommand stub is replaced entirely.

## Spec gap flagged for agent: `--pos` name mapping

The `--pos` option accepts human-readable names (`noun`, `adjective`) but the NLP pipeline uses spaCy universal POS tags (`NOUN`, `ADJ`). The implementing agent must define and test the mapping table. Canonical spaCy tags in use: `NOUN`, `VERB`, `ADJ`, `ADV`, `PROPN`, `PRON`, `CCONJ`, `SCONJ`, `ADP`, `INTJ`.

## Pipeline execution order

```
reader_for(INPUT).read()
→ nlp_pipeline.process(text)
→ counter.count(tokens)
→ filter.apply_stopwords(counts, stopwords_path)  # if --stopwords given
→ ranker.rank(pos_counts, top_n)                  # per POS
→ writer.write(ranked, output_path, split=--split)
→ html_reporter.render(counts, ranked, report_path, ranker_name)  # if --html-report
```

## Files to modify/create

- `src/book_munger/cli.py` — full replacement of the current stub
- `tests/test_cli.py` — expand existing tests; add integration test

## Integration test convention

Synthetic fixture only — generate a small in-memory text, write to `tmp_path`, run CLI against it, assert output files are created. No Project Gutenberg books.

## Verification

```bash
pytest tests/test_cli.py -v
book-munger --help
book-munger <synthetic-fixture> --html-report
pytest  # full suite
```
