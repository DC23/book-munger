# 0006: CLI as single command with positional input

**Status:** Accepted

## Context

Issue #10 specifies the full CLI implementation. The initial stub (issue #2) used `@click.group()` with a `process` subcommand, leaving the long-term command structure open. As the CLI was planned in detail, the question arose: retain the group and add a subcommand (e.g. `book-munger generate`), or flatten to a single command (`book-munger INPUT`)?

The tool does one thing: transform a book into word tables. There is no second action that would justify a command group at this stage.

## Decision

`cli.py` implements a single `@click.command()`. The source file is a positional argument (`INPUT`), not a `--input` option. The `process` subcommand stub is removed entirely. The `@click.group()` wrapper is dropped.

## Consequences

- Help output is simpler and the usage line is immediately clear: `book-munger INPUT [OPTIONS]`
- Reader format auto-detection (`reader_for()`) means the positional argument needs no type qualifier
- If a second top-level action is ever needed, this would require introducing a group and is a breaking CLI change — acceptable given the project's scope
