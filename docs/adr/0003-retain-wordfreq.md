# 0003: Retain wordfreq as a long-term dependency

**Status:** Accepted

## Context

After noting that `wordfreq` is in sunset mode (data frozen ~2021, packaging-only updates), the deferred question was whether to replace it with NLTK `FreqDist` on the source corpus. Issue #11 (`DistinctivenessRanker`) resolves this: the distinctiveness score algorithm is `corpus_count / zipf_frequency(lemma, "en")`, where `zipf_frequency` is `wordfreq`'s pre-computed general-English log-scale frequency. NLTK `FreqDist` operates on a supplied corpus and cannot serve as a drop-in general-language baseline.

## Decision

Retain `wordfreq`. It is not a candidate for replacement by NLTK `FreqDist` — the two serve different roles. `wordfreq` provides the general-English baseline; NLTK `FreqDist` (if used at all) would provide corpus-specific frequency. They are complementary, not alternatives.

## Consequences

- `wordfreq` stays as a runtime dependency for the foreseeable future.
- Sunset risk is accepted: the frequency data is frozen but stable; if `wordfreq` becomes uninstallable, the general-language baseline would need to be sourced from a static dataset (e.g. a bundled Zipf table), not from NLTK.
- Remove any "evaluate wordfreq vs NLTK FreqDist" TODO comments when they appear — the decision is made.
