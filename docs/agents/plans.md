# Plans

How the engineering skills should save and index in-progress plans for this project.

**If `docs/plans/` or `docs/plans/INDEX.md` don't exist, proceed silently.** Create them only when an incomplete plan needs preserving.

## Naming convention

`YYYY-MM-DD-HHMM-description.md` — timestamp prefix, hyphen-separated description, e.g. `2026-05-27-1430-equipment-extraction.md`. Files live in `docs/plans/`.

## Index format

Append one line to `docs/plans/INDEX.md` when saving a plan:

```
- [YYYY-MM-DD-HHMM-description.md](YYYY-MM-DD-HHMM-description.md) — topic, topic, symbol
```

Topics should be enough to locate the plan without opening it — scope, key files, phase or feature name.

## Document structure

Not prescribed. Write whatever structure suits the plan — task lists, decision trees, open questions, step-by-step approaches. The index entry is the only required convention.
