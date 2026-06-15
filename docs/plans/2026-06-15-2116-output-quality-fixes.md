# Plan: Post-pipeline output quality fixes

## Context

First real-book runs of the full pipeline revealed five output quality problems:
1. Punctuation tokens (`.`, `!`, `-`, `´`) appearing in word tables — spaCy mis-tags some punctuation as PROPN or NOUN.
2. Common words filling every POS column — the `--stopwords` flag exists but no defaults run when it's omitted.
3. `chapter` appearing in some frequency tables — an artefact of chapter heading text flowing through the pipeline; deferred until stopwords are addressed.
4. Column ordering in combined tables is inconsistent across books — `counter.count()` builds a dict in token-encounter order, so which POS appears first depends on the text.
5. POS column headers in the output tables are hard to decode — a quick-reference table in the README would help.

This plan covers six GitHub issues to create (not implement now). Issues A, B, D, and E are independent; Issue C is blocked on B; Issue F is blocked on A and B.

---

## Issue A — Punctuation guard in NLP pipeline (issue #27)

**Problem:** Tokens whose text or lemma is purely punctuation slip through `_ALLOWED_POS` filtering because spaCy occasionally mis-tags them (e.g. isolated `-` tagged PROPN).

**Fix:** In `nlp_pipeline.process()`, add a guard that skips any token whose lemma contains no alphabetic character:

```python
if not any(c.isalpha() for c in token.lemma_):
    continue
```

Insert this check inside the existing `if token.pos_ in _ALLOWED_POS` branch, or as an additional condition. Checking the lemma (not the raw text) is the right target because the counter operates on lemmas.

**Files:** `src/book_munger/nlp_pipeline.py`, `tests/test_nlp_pipeline.py`

**Tests:** The existing test `test_punctuation_excluded` covers PUNCT-tagged tokens; add a new parametrised case covering mis-tagged punctuation that passes the POS filter but has a non-alpha lemma.

---

## Issue B — Stopwords infrastructure (issue #28)

**Decisions:**
- No `--stopwords` → use spaCy's built-in English stop words automatically.
- `--stopwords FILE` → load that file and use it instead (full override, not additive).
- Ship a curated default stopwords file in the repo as a convenience; it is never auto-loaded — users opt in by passing it to `--stopwords`.

### filter.py refactor

Split the current monolithic `apply_stopwords(counts, stopwords_path)` into three focused functions:

```python
def load_stopwords(path: Path) -> set[str]:
    """Load stopwords from a text file (one per line, # comments ignored)."""
    ...

def spacy_stopwords() -> set[str]:
    """Return spaCy's built-in English stop word set."""
    from spacy.lang.en.stop_words import STOP_WORDS
    return set(STOP_WORDS)

def apply_stopwords(counts: dict[str, dict[str, int]], stopwords: set[str] | None) -> dict[str, dict[str, int]]:
    """Filter counts; identity if stopwords is None or empty."""
    ...
```

`apply_stopwords` now takes a pre-resolved `set[str]` instead of a `Path`. This is a signature change — existing tests for this function need updating (they currently write temp files; they can pass sets directly instead, which is simpler).

**File:** `src/book_munger/filter.py`, `tests/test_filter.py`

### cli.py wiring

```python
if stopwords_path:
    stopwords = filter.load_stopwords(stopwords_path)
else:
    stopwords = filter.spacy_stopwords()
counts = filter.apply_stopwords(counts, stopwords)
```

The `--stopwords` CLI option remains unchanged (optional path argument). Default behaviour changes: previously no filtering ran when omitted; now spaCy defaults run.

**File:** `src/book_munger/cli.py`, `tests/test_cli.py`

Test implications:
- Existing `--stopwords` CLI test: still valid, just passes a file.
- Add a test asserting that common words from `spacy_stopwords()` are absent when `--stopwords` is not supplied.
- Update any CLI tests that assert exact ranked output (spaCy defaults now run by default).

### Bundled stopwords file

Ship a curated stopwords file at `src/book_munger/data/stopwords-en.txt`. The user seeds this from the spaCy list plus words observed in the unfiltered output. Format matches the existing file reader: one word per line, `#` comments allowed.

Add to `pyproject.toml`:
```toml
[tool.setuptools.package-data]
book_munger = ["data/*.txt"]
```

The file is not auto-loaded by the CLI. Users reference it explicitly by path. Document its location in the README.

---

## Issue C — Chapter heading filtering (issue #31, deferred, blocked on B)

**Context:** ADR 0004 deferred heading removal on the assumption that `chapter` would be suppressed by the wordfreq baseline. Real-book runs show this assumption does not hold for `DistinctivenessRanker` or high-frequency books.

**Defer until:** After Issue B lands and tables are re-run. If `chapter` disappears from outputs with stopwords active (by including it in the curated file), this issue may close without code changes.

**If still needed:** Conservative starting point — strip `<h1>`–`<h6>` elements in `HtmlReader.read()` before calling `get_text()`:

```python
for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
    tag.decompose()
```

This is format-specific (HTML only) and stays within the existing Reader responsibility boundary from ADR 0004. `PlainTextReader` would not change.

ADR 0004 should be updated (or a new ADR written) if this goes ahead, noting that the wordfreq suppression assumption proved incorrect in practice.

**File:** `src/book_munger/readers/html.py`, `docs/adr/0004-...`

---

## Issue D — Consistent POS column ordering (issue #29)

**Problem:** `counter.count()` builds a dict in token-encounter order (first POS seen wins), so combined table column sequence varies book to book.

**Fix:** Define a canonical POS order constant and apply it in `MarkdownWriter._write_combined()` when building headers and columns. Any POS present in `ranked` but absent from the canonical list falls back to the end (preserving forward compatibility if new POS tags are ever added).

Canonical order (content words first, function words after):

```python
_COLUMN_ORDER = [
    "PROPN", "NOUN", "VERB", "ADJ", "ADV",
    "PRON", "ADP", "CCONJ", "SCONJ", "INTJ",
]
```

In `_write_combined()`, sort `ranked.items()` against this order before building `headers` and `columns`:

```python
ordered = sorted(ranked.items(), key=lambda kv: _COLUMN_ORDER.index(kv[0]) if kv[0] in _COLUMN_ORDER else len(_COLUMN_ORDER))
headers = [_pos_label(pos) for pos, _ in ordered]
columns = [words for _, words in ordered]
```

**Files:** `src/book_munger/writers/markdown.py`, `tests/test_writers.py`

**Tests:** Assert that a `ranked` dict with keys supplied in arbitrary order produces columns in the canonical sequence. Also verify that an unknown POS key appended to the end rather than raising.

---

## Issue E — POS reference table in README (issue #30, docs only, no code)

**Problem:** Column headers like `Cconj`, `Sconj`, `Adp` are not self-explanatory, particularly for infrequent users.

**Fix:** Add a short reference table to `README.md` mapping each column label to its full name and a brief description. No code changes.

| Column label | Part of speech | What it contains |
|---|---|---|
| Propn | Proper noun | Named people, places, organisations |
| Nouns | Common noun | Concrete and abstract things |
| Verbs | Verb | Actions and states |
| Adjectives | Adjective | Describing words |
| Adverbs | Adverb | Modifiers of verbs, adjectives, or other adverbs |
| Pron | Pronoun | Substitutes for nouns (he, she, it, they…) |
| Adp | Adposition | Prepositions and postpositions (in, of, through…) |
| Cconj | Coordinating conjunction | Links equal elements (and, but, or, yet…) |
| Sconj | Subordinating conjunction | Introduces clauses (if, when, because, although…) |
| Intj | Interjection | Exclamations and discourse markers (oh, alas, yes…) |

**File:** `README.md`

---

## Issue F — Blended ranker (issue #32, post-processing union, deferred)

**Motivation:** For some books (observed first with *At the Mountains of Madness*), neither pure frequency nor pure distinctiveness ranking alone produces the most evocative Word Table. Frequency captures texture (words the author reaches for repeatedly); distinctiveness captures fingerprint (words rare in general English). A blend of both covers the sweet spot.

**Approach:** Post-processing union, not a new scoring function. Take the top N words from each existing Ranker, union the two lists, deduplicate, sort alphabetically for human readability.

This composes on top of the existing `FrequencyRanker` and `DistinctivenessRanker` without touching their internals. A new `--ranker blended` option would invoke this path; the `ranker_for()` factory would need extending.

**Defer until:** After Issues A and B are implemented and real-book output is reassessed with clean tables. The right top-N value and whether alphabetic sort is sufficient are easier to judge from cleaner data.

**Files (when ready):**
- `src/book_munger/rankers/blended.py` (new)
- `src/book_munger/rankers/__init__.py`
- `src/book_munger/cli.py`
- `tests/test_rankers.py`

---

## Issue sequencing

| Issue | GitHub | Dependency | Notes |
|---|---|---|---|
| A — Punctuation guard | #27 | None | Small, independent |
| B — Stopwords infrastructure | #28 | None | Independent of A; larger scope |
| C — Chapter headings | #31 | B (observe output first) | May not be needed |
| D — Column ordering | #29 | None | Small, independent |
| E — README POS reference | #30 | None | Docs only, trivial |
| F — Blended ranker | #32 | A + B (reassess with clean output) | Defer; calibration depends on clean tables |
