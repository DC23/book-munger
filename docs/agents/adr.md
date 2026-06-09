# ADRs

How the engineering skills should write and maintain Architecture Decision Records for this project.

**If `docs/adr/` or `docs/adr/INDEX.md` don't exist, proceed silently.** Create them only when a decision actually warrants recording.

## Naming convention

`NNNN-kebab-case-title.md` — four-digit zero-padded sequential number, e.g. `0001-description-format.md`. Files live in `docs/adr/`.

Check `docs/adr/INDEX.md` before writing a new ADR to confirm the next number and avoid duplicates.

## Document format

```markdown
# NNNN: Title

**Status:** Accepted | Deprecated | Superseded by NNNN

## Context

Why the decision was needed.

## Decision

What was decided.

## Consequences

What follows from the decision — trade-offs accepted, constraints created.
```

Keep each section brief. An ADR that needs more than a few sentences per section is probably covering too much ground. Write the ADR when the decision is made, not speculatively.

## Index format

Append one line to `docs/adr/INDEX.md` when writing a new ADR:

```
- [NNNN-title.md](NNNN-title.md) — topic, topic, symbol
```

Topics should include key symbols affected (function names, config keys, field names) — enough to locate the ADR without opening it.

## Flag conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0007 (example decision) — but worth reopening because…_
