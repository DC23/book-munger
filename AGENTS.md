# book-munger agent instructions

## Python environment

All Python work uses the local virtual environment at `.venv/`. Never install packages to system Python.

- Activate: `source .venv/bin/activate`
- Run tools directly: `.venv/bin/python`, `.venv/bin/pytest`, `.venv/bin/pip`
- Install deps after creating/cloning: `pip install -e .[dev]` (with venv active)

## Agent skills

### Issue tracker

Issues live in GitHub Issues (`DC23/book-munger`). See `docs/agents/issue-tracker.md`.

### Triage labels

Default DC23 label vocabulary — no overrides. See `docs/agents/triage-labels.md`.

When creating issues: always apply `needs-triage`. Also apply `roadmap` for planned features and maintainer-initiated work. Apply `epic` (alongside `roadmap`) for parent issues that track a collection of sub-issues — epics have no implementation surface and should not be put through the triage state machine. Use `/grill-with-docs` or plan mode to work on an epic instead.

When creating groups of related issues (epic breakdowns, dependency chains), set parent and blocked-by relationships via `gh api graphql`. The `gh issue` subcommand has no native flags for this. Verified mutations:

```bash
# Get node IDs
gh api graphql -f query='{ repository(owner: "DC23", name: "book-munger") { issue(number: N) { id } } }'

# Make CHILD a sub-issue of PARENT
gh api graphql -f query='mutation { addSubIssue(input: {issueId: "PARENT_ID", subIssueId: "CHILD_ID"}) { issue { number } subIssue { number } } }'

# Mark ISSUE as blocked by BLOCKER
gh api graphql -f query='mutation { addBlockedBy(input: {issueId: "ISSUE_ID", blockingIssueId: "BLOCKER_ID"}) { clientMutationId } }'

# Remove CHILD from PARENT's sub-issues
gh api graphql -f query='mutation { removeSubIssue(input: {issueId: "PARENT_ID", subIssueId: "CHILD_ID"}) { clientMutationId } }'

# Remove blocked-by relationship (ISSUE is no longer blocked by BLOCKER)
gh api graphql -f query='mutation { removeBlockedBy(input: {issueId: "ISSUE_ID", blockingIssueId: "BLOCKER_ID"}) { clientMutationId } }'
```

### Domain docs

Single-context layout: `docs/DOMAIN_DICTIONARY.md`, `docs/adr/` for decisions. See `docs/agents/domain.md`.

## Testing conventions

Do not use real Project Gutenberg books as test fixtures. Copyright status outside the US is ambiguous, and PG silently re-encodes old files to UTF-8 during maintenance updates, making them unreliable for encoding tests. Use synthetic fixtures generated programmatically (e.g. via pytest `tmp_path`) with Lorem Ipsum body text and minimal PG-format structure.
