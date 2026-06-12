# 0002: Click for CLI framework

**Status:** Accepted

## Context

The project needs a CLI entry point. Options included argparse (stdlib), Click, and Typer. The project already pulls in spaCy, which transitively depends on Typer — however Typer's API is built on Click under the hood.

## Decision

Use Click directly. The `book-munger` console script entry point is `book_munger.cli:cli`, a `@click.group()`.

## Consequences

- Click is an explicit runtime dependency.
- Sub-commands are added as `@cli.command()` decorated functions in `cli.py` or registered from sub-modules.
- Typer remains available transitively via spaCy but is not used — avoids coupling the CLI surface to a transitive dep.
