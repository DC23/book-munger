# Handoff Index

- [2026-06-13-0957-scaffolding.md](2026-06-13-0957-scaffolding.md) — issue #2, project scaffolding, pyproject.toml, src layout, Click CLI, venv, wordfreq, ADR 0001, ADR 0002
- [2026-06-13-1745-text-loader-reader-pattern.md](2026-06-13-1745-text-loader-reader-pattern.md) — issue #3, Reader pattern, PlainTextReader, HtmlReader, reader_for, beautifulsoup4, issue #4 closed, ADR 0004, ADR 0005
- [2026-06-13-1810-text-loader-implementation.md](2026-06-13-1810-text-loader-implementation.md) — issue #3 implemented, TDD, readers package, process CLI command, commit ded78c4, synthetic fixture approach confirmed
- [2026-06-13-1820-nlp-pipeline.md](2026-06-13-1820-nlp-pipeline.md) — issue #5 implemented, TDD, pipeline.py, process(), lru_cache, spaCy, en_core_web_sm, lemma/POS, commit 84daa31
- [2026-06-13-2022-counter-filter.md](2026-06-13-2022-counter-filter.md) — issue #6 implemented, TDD, counter.py, filter.py, count(), apply_stopwords(), stopword file format, commits 98d432e/3861d66
- [2026-06-13-2216-ranker-base-class-and-frequency-ranker.md](2026-06-13-2216-ranker-base-class-and-frequency-ranker.md) — issue #7 implemented, TDD, rankers package, BaseRanker, FrequencyRanker, plan review, triage, commits 65546f1/f52e74e, PR #20
- [2026-06-14-1115-issue-drift-checks-and-triage.md](2026-06-14-1115-issue-drift-checks-and-triage.md) — issues #8 #9 #10 #11 drift-checked and triaged ready-for-agent, BaseWriter, MarkdownWriter combined/split, CLI single command positional input, default ranker distinctive, ADR 0006, plans 0000–0003
- [2026-06-14-1451-issue-11-distinctiveness-ranker.md](2026-06-14-1451-issue-11-distinctiveness-ranker.md) — issue #11 implemented, DistinctivenessRanker, zipf_frequency, TDD 5 tests, ranker_for() spec gap added to plan #10, commits 6f0b019/1f81f51
- [2026-06-14-1655-issue-9-writer-issue-8-reporter.md](2026-06-14-1655-issue-9-writer-issue-8-reporter.md) — issue #9 BaseWriter/MarkdownWriter merged PR #24, issue #8 HTML ranker report commit d3c1ae4 pending PR, 60 tests, #10 CLI deferred
- [2026-06-14-1745-issue-10-cli-interface.md](2026-06-14-1745-issue-10-cli-interface.md) — issue #10 CLI interface, ranker_for() factory, _POS_NAMES mapping, single command, full pipeline wiring, README usage guide, 73 tests, epic #1 complete pending PR merge
