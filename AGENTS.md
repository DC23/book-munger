## Agent skills

### Issue tracker

Issues live in GitHub Issues (`DC23/book-munger`). See `docs/agents/issue-tracker.md`.

### Triage labels

Default DC23 label vocabulary — no overrides. See `docs/agents/triage-labels.md`.

When creating issues: always apply `needs-triage`. Also apply `roadmap` for planned features and maintainer-initiated work.

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
