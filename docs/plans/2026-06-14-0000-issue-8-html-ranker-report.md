# Plan: HTML Ranker Report (issue #8)

## Context

Issue #8 was drafted before the Ranker strategy pattern was finalised in #7. Its original framing ("HTML frequency report") is now wrong: the report must surface the output of whichever Ranker strategy was applied, not just raw frequency data. The issue is now blocked by #11 (DistinctivenessRanker) by sequencing preference. The reporter interface works with any Ranker.

The core acceptance criteria from the issue (signature, Jinja2 template, TDD test file) remain valid — only the conceptual framing and one parameter need updating.

## What changes from the original issue

| Original | Revised |
|----------|---------|
| "HTML frequency report" | "HTML ranker report" |
| Report title: word frequencies | Report title: ranked word output |
| No ranker context shown | Optional `ranker_name` param surfaced in report header |

`BaseRanker` has no `name` property (`src/book_munger/rankers/base.py`), so the caller must supply the name explicitly.

## Revised render() signature

```python
def render(
    counts: dict[str, dict[str, int]],   # {pos: {lemma: count}} from Counter/Filter
    ranked: dict[str, list[str]],         # {pos: [lemma, ...]} from Ranker
    output_path: Path,
    ranker_name: str = "",                # display name of the Ranker, e.g. "FrequencyRanker"
) -> None:
```

`ranked` drives the output — only POS types present in `ranked` appear in the report. Counts are looked up from `counts[pos][lemma]` for each ranked lemma.

## Files to create

```
src/book_munger/reporters/__init__.py          (empty)
src/book_munger/reporters/html.py              (render() function)
src/book_munger/reporters/templates/
    report.html.j2                             (Jinja2 template)
tests/test_html_reporter.py
```

No new dependencies — `jinja2>=3.0` is already in `pyproject.toml`.

Template location: `Path(__file__).parent / "templates" / "report.html.j2"` (editable install).

## Report structure (template)

- `<title>`: "Word Ranking Report" (with `— {ranker_name}` appended if provided)
- **Summary section**: total tokens (sum of all count values), vocabulary size (total unique lemmas across all POS), POS breakdown table (POS | lemma count | token count)
- **Per-POS sections**: one table per POS in `ranked`: columns Rank | Lemma | Count
  - Rank is 1-indexed position in `ranked[pos]`
  - Count comes from `counts[pos][lemma]`
- Minimal inline `<style>` block — readable in a browser, no external CSS

## Tests (TDD — write red tests first)

`tests/test_html_reporter.py`:

1. Output file is created at `output_path`
2. Known lemmas from `ranked` appear in the HTML
3. Rank order matches list order (position 0 → rank 1)
4. Summary stats (total tokens, vocab size) are correct
5. `ranker_name` appears in output when provided; absent when `""`
6. Writing to a non-existent directory raises `FileNotFoundError`

Use `tmp_path` fixture, synthetic counts dict — no real books.

## Verification

```bash
pytest tests/test_html_reporter.py -v
```

Browser smoke-test: call `render()` with synthetic data and open the resulting `.html` file.

## Note on domain vocabulary

"Reporter" is not yet in `DOMAIN_DICTIONARY.md`. It sits outside the Pipeline (which ends at Ranker). Flag for the next `/domain-review` session.
