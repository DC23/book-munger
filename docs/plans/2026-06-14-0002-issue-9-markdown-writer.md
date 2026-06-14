# Plan: Markdown writer — base class and first implementation (issue #9)

## Context

Issue #9 was written when only split output (one file per POS) was considered. The user has since confirmed that combined output (all POS in one file) is the default. The issue is also updated to follow the `Base` prefix convention used by `BaseRanker` and `BaseReader`.

## Drift fixes applied to issue

1. `Writer(ABC)` → `BaseWriter(ABC)`, `MarkdownWriter(Writer)` → `MarkdownWriter(BaseWriter)`
2. Scope expanded to cover both split and combined output modes

## Files to create

```
src/book_munger/writers/__init__.py          (empty)
src/book_munger/writers/base.py              (BaseWriter ABC)
src/book_munger/writers/markdown.py          (MarkdownWriter)
tests/test_markdown_writer.py
```

## Revised BaseWriter interface

```python
class BaseWriter(ABC):
    @abstractmethod
    def write(self, ranked: dict[str, list[str]], path: Path, split: bool = False) -> None:
        """Write ranked word lists. split=False: combined file; split=True: one file per POS."""
```

The Writer always receives the full `{pos: [lemma, ...]}` ranked dict and handles routing internally. This matches how the CLI will invoke it (passing all POS at once with a split flag).

## Output formats

**Combined (default, `split=False`):**
A single Markdown file. Exact column format TBD by agent — a Markdown table with POS as column headers and words in rows is the natural choice.

**Split (`split=True`):**
One file per POS. Filename derived from `path` stem + POS label (e.g. `book-nouns.md`, `book-adjectives.md`). Each file:
```markdown
# Nouns (top 100)
sea
night
hand
```

## Tests (TDD)

`tests/test_markdown_writer.py`:

1. Combined mode: output file is created at `path`
2. Combined mode: all POS sections/columns appear in output
3. Combined mode: word order matches `ranked` list order
4. Split mode: one file created per POS in `ranked`
5. Split mode: each file has correct header and words in order
6. Empty `ranked` dict writes without error
7. Invalid path raises appropriate error

Use `tmp_path`, synthetic data — no real books.

## Pattern to follow

`FrequencyRanker` / `BaseRanker` as the strategy pattern analogue. `MarkdownWriter` mirrors how `FrequencyRanker` extends `BaseRanker`.

## Verification

```bash
pytest tests/test_markdown_writer.py -v
pytest  # full suite
```
