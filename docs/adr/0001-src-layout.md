# 0001: src layout

**Status:** Accepted

## Context

The package could be laid out as a flat `book_munger/` directory at the repo root, or under `src/book_munger/`. The flat layout allows accidental import of the uninstalled package from the repo root, masking missing dependencies.

## Decision

Use a `src/` layout: `src/book_munger/`. Setuptools is configured with `[tool.setuptools.packages.find] where = ["src"]`.

## Consequences

- Importing `book_munger` before running `pip install -e .` raises `ModuleNotFoundError`, making installation a hard requirement.
- All source lives under `src/`; tests live at `tests/` alongside it.
