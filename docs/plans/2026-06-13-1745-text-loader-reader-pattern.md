# Plan: Reader Pattern for Issue #3 (Text Loader)

## Context

Issue #3 implements the input side of the text processing pipeline. The project ingests Project Gutenberg books and produces thematic word frequency tables. Two input formats exist: plain text (`.txt`) and zipped HTML (`.zip` containing a single `.html` file). The HTML format provides explicit `id="pg-header"` / `id="pg-footer"` div IDs that make boilerplate stripping more reliable than regex-based approaches on text files. A Reader pattern mirrors the Writer pattern planned for output (issue #9) and provides a clean extension point for future formats (EPUB, ODT, etc.).

Decisions confirmed:

- Readers return a plain `str` (structure deferred until a concrete downstream need exists)
- Boilerplate stripping is the Reader's responsibility — it's format-specific and quality improves by binding the two together

## Design

### Package layout

```text
src/book_munger/
    readers/
        __init__.py      # exports BaseReader, reader_for()
        base.py          # abstract BaseReader
        plaintext.py     # PlainTextReader
        html.py          # HtmlReader (handles .html and .zip)
```

### BaseReader interface

```python
from abc import ABC, abstractmethod
from pathlib import Path

class BaseReader(ABC):
    def __init__(self, path: Path) -> None:
        self.path = path

    @abstractmethod
    def read(self) -> str:
        """Return cleaned book text as a plain string with boilerplate removed."""
```

### Factory function

```python
def reader_for(path: Path) -> BaseReader:
    suffix = path.suffix.lower()
    if suffix in ('.html', '.htm', '.zip'):
        return HtmlReader(path)
    return PlainTextReader(path)
```

Dispatch by suffix. `.zip` is assumed to contain HTML (PG convention); add a content-sniff guard if needed later.

### PlainTextReader

- Encoding: try UTF-8, fall back to `latin-1` (covers all known PG text files without adding a detection dependency)
- Boilerplate strip: slice on `*** START OF THE PROJECT GUTENBERG EBOOK` and `*** END OF THE PROJECT GUTENBERG EBOOK` — both markers are consistent across the 1995–2023 test corpus
- Return the slice between those markers, stripped of leading/trailing whitespace

### HtmlReader

- New dependency: `beautifulsoup4` (add to `pyproject.toml` under `[project.dependencies]`)
- If path is `.zip`: open with `zipfile.ZipFile`, read the single `.html` member into memory
- Parse with `BeautifulSoup(html_bytes, 'html.parser')` (stdlib parser, no lxml needed)
- Strip boilerplate: `soup.find(id='pg-header').decompose()` and `soup.find(id='pg-footer').decompose()`
- Return `soup.get_text(separator='\n', strip=True)`

Both `decompose()` calls should guard against `None` (older or non-PG HTML may lack these IDs).

### CLI integration

Add a `process` sub-command to the existing Click group in `src/book_munger/cli.py`:

```python
@cli.command()
@click.argument('input_file', type=click.Path(exists=True, path_type=Path))
def process(input_file):
    """Process a book and produce a word frequency table."""
    reader = reader_for(input_file)
    text = reader.read()
    ...
```

## Files to create / modify

| File | Action |
| --- | --- |
| `src/book_munger/readers/__init__.py` | Create — export `BaseReader`, `reader_for` |
| `src/book_munger/readers/base.py` | Create — abstract `BaseReader` |
| `src/book_munger/readers/plaintext.py` | Create — `PlainTextReader` |
| `src/book_munger/readers/html.py` | Create — `HtmlReader` |
| `src/book_munger/cli.py` | Modify — add `process` command |
| `pyproject.toml` | Modify — add `beautifulsoup4>=4.12` to dependencies |
| `tests/test_readers.py` | Create — unit tests (see below) |

## Tests

Use synthetic fixtures generated in `tests/conftest.py` via pytest's `tmp_path` fixture. No real PG books — copyright is ambiguous outside the US, and PG has been silently re-encoding old files to UTF-8, making them unreliable for encoding tests anyway.

### Synthetic fixture content

**PG plain text structure** (UTF-8 and latin-1 variants):
```
The Project Gutenberg eBook of Lorem Ipsum

[metadata lines]

*** START OF THE PROJECT GUTENBERG EBOOK LOREM IPSUM ***

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

*** END OF THE PROJECT GUTENBERG EBOOK LOREM IPSUM ***

[footer boilerplate]
```

**PG HTML structure**:
```html
<html><body>
<div id="pg-header">Project Gutenberg header content</div>
<p>Lorem ipsum dolor sit amet.</p>
<div id="pg-footer">Project Gutenberg footer content</div>
</body></html>
```

Zip fixture: `zipfile.ZipFile` written to `tmp_path` containing the HTML string above.

### Test cases

- `PlainTextReader` on UTF-8 fixture — header/footer lines absent, Lorem Ipsum content present
- `PlainTextReader` on latin-1 fixture (bytes written with `encoding='latin-1'`, content includes `\xe9` café-style character) — no `UnicodeDecodeError`, character present in output
- `HtmlReader` on `.html` fixture — `pg-header`/`pg-footer` text absent, Lorem Ipsum present
- `HtmlReader` on `.zip` fixture — same assertions via zip path
- `HtmlReader` on HTML without PG divs — no error (graceful `None` guard on `decompose()`)
- `reader_for()` dispatch — `.txt` → `PlainTextReader`, `.html` → `HtmlReader`, `.zip` → `HtmlReader`

Run with: `.venv/bin/pytest tests/test_readers.py -v`
