# Handoff: 2026-06-14-1115 Issue drift checks and triage

## Summary

**Baseline:** 41 tests passing (clean, no code changes this session — planning and triage only)

---

## What happened

This was a planning and triage session. No implementation work was done. The goal was to drift-check all remaining unimplemented issues (#8, #9, #10, #11) against the current codebase state, update their specs, write implementation plans, and triage them to `ready-for-agent`.

All four issues are now triaged and have implementation plans in `docs/plans/`.

---

## Drift findings per issue

### Issue #8 — HTML ranker report

The issue was written as a "frequency report" before the Ranker strategy pattern was finalised in #7. Key fixes:

- Renamed concept: "HTML frequency report" → "HTML ranker report"
- Added `ranker_name: str = ""` parameter to `render()` — `BaseRanker` has no name property, so the caller supplies it
- Replaced the original 3-parameter signature with the 4-parameter version

Issue is now `roadmap` + `ready-for-agent` + `blocked` (blocked by #11 in GitHub).

### Issue #11 — DistinctivenessRanker

Two drift points against the current code:

- AC referenced `DistinctivenessRanker(Ranker)` — base class is `BaseRanker`
- Verification section assumed `--ranker frequency` / `--ranker distinctive` CLI flags that don't exist yet

Both fixed. Issue is now `roadmap` + `ready-for-agent`.

### Issue #9 — Markdown writer

Two changes:

1. `Writer(ABC)` → `BaseWriter(ABC)`, `MarkdownWriter(Writer)` → `MarkdownWriter(BaseWriter)` — follows `Base` prefix convention (`BaseRanker`, `BaseReader`)
2. **Scope expansion**: the original issue specified split output only (one file per POS). The maintainer confirmed combined output (all POS in one file) is the default, with split as an opt-in mode. `BaseWriter.write()` was redesigned to accept the full `{pos: [lemma, ...]}` ranked dict rather than a single POS list, with a `split: bool = False` parameter.

Issue is now `roadmap` + `ready-for-agent`.

### Issue #10 — CLI interface

Most significantly revised. Key changes from the original spec:

| Original | Revised |
|----------|---------|
| `@click.group()` — structure unspecified | Single `@click.command()` — `book-munger INPUT [OPTIONS]` |
| `--input PATH` option | Positional `INPUT` argument |
| Default ranker: `frequency` | Default ranker: `distinctive` |
| HTML report always generated | `--html-report` flag, default off |
| Output path only | `--output PATH` + `--output-name NAME` (defaults to input stem) |
| No combined/split distinction | `--split` flag; default is combined output |

One bounded spec gap delegated to the implementing agent: `--pos` accepts human-readable names (`noun`, `adjective`) but the NLP pipeline uses spaCy tags (`NOUN`, `ADJ`). The agent must define and test the mapping. Canonical tags in use: `NOUN VERB ADJ ADV PROPN PRON CCONJ SCONJ ADP INTJ`.

Issue is now `roadmap` + `ready-for-agent`.

---

## Artefacts created

**Plans (docs/plans/):**
- `2026-06-14-0000-issue-8-html-ranker-report.md`
- `2026-06-14-0001-issue-11-distinctiveness-ranker.md`
- `2026-06-14-0002-issue-9-markdown-writer.md`
- `2026-06-14-0003-issue-10-cli-interface.md`

**ADR:**
- `docs/adr/0006-cli-single-command-with-positional-input.md` — single `@click.command()`, positional INPUT, `process` stub removed

**Domain candidates added:**
- `Writer` — output strategy component, mirrors Reader pattern
- `Reporter` — HTML report generator, optional diagnostic artefact outside the Pipeline

---

## Implementation sequence

The epic dependency graph is:

```
#9 (BaseWriter + MarkdownWriter)  ─┐
#11 (DistinctivenessRanker)        ├──► #10 (CLI)
#8 (HTML reporter)  ← blocked by #11 ─┘
```

#9 and #11 are parallelisable. #8 is ready to implement once #11 is done (the reporter interface works with any Ranker, but the maintainer set the sequencing dependency deliberately). #10 integrates everything and goes last.

---

## Minor housekeeping

`response.md` was created in the project root during this session as a user input artefact. It contains the CLI design notes from the maintainer. It is not tracked by git and can be deleted or left in place — it is not a project document.

---

## Discussion: autonomous agent sequencing

The maintainer asked whether updating the GitHub PAT with PR R/W permissions would enable an agent to work through the issues autonomously. Short answer: yes mechanically, with two caveats:

1. Check whether `main` has branch protection rules requiring reviews or CI status checks before merge (`gh api repos/DC23/book-munger/branches/main/protection`)
2. The current per-issue briefs won't chain automatically — you'd need either an orchestrating brief covering all four in sequence, or a hook/trigger between sessions

The maintainer's current per-issue approach is well-suited to the project's current state, where design decisions are still crystallising at implementation time (e.g. the `--pos` mapping gap in #10, the exact combined-output format in #9).
