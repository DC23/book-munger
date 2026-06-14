# book-munger
Python application that ingests text documents to compile word frequency lists to generate genre-specific spark tables for use in solo RPG games

## Setup

```bash
pip install -e .[dev]
python -m spacy download en_core_web_sm
```

## Usage

```
book-munger INPUT_FILE [OPTIONS]
```

Reads `INPUT_FILE` (plain text or HTML; format auto-detected), runs it through the NLP pipeline, and writes a Markdown word table to the output directory.

```bash
# Basic — produces sample.md in the current directory
book-munger sample.txt

# Specify output directory and limit to 50 words per part of speech
book-munger sample.txt --output tables/ --top-n 50

# Use the frequency ranker instead of the default distinctiveness ranker
book-munger sample.txt --output tables/ --ranker frequency

# Filter to nouns and adjectives only, write one file per POS
book-munger sample.txt --output tables/ --pos noun,adjective --split

# Also generate an HTML diagnostic report
book-munger sample.txt --output tables/ --html-report
```

### Options

| Option | Default | Description |
| --- | --- | --- |
| `--output PATH` | current directory | Output directory |
| `--output-name NAME` | input file stem | Override the output filename root |
| `--stopwords PATH` | _(none)_ | Stopword list; one word per line, `#` for comments |
| `--top-n INT` | 100 | Words per part-of-speech list |
| `--pos TEXT` | _(all)_ | Comma-separated POS filter: `noun`, `verb`, `adjective`, `adverb`, `propnoun`, `pronoun`, `cconj`, `sconj`, `adposition`, `interjection` |
| `--ranker TEXT` | `distinctive` | Ranking strategy: `distinctive` or `frequency` |
| `--split` | combined | Write one file per POS instead of a combined table |
| `--html-report` | off | Also write an HTML diagnostic report alongside the word table |
