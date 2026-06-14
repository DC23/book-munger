from pathlib import Path

import click

from book_munger import counter
from book_munger import filter as _filter
from book_munger import nlp_pipeline
from book_munger.rankers import ranker_for
from book_munger.readers import reader_for
from book_munger.reporters import html as html_reporter
from book_munger.writers.markdown import MarkdownWriter

_POS_NAMES = {
    "noun": "NOUN",
    "verb": "VERB",
    "adjective": "ADJ",
    "adverb": "ADV",
    "propnoun": "PROPN",
    "pronoun": "PRON",
    "cconj": "CCONJ",
    "sconj": "SCONJ",
    "adposition": "ADP",
    "interjection": "INTJ",
}


@click.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.option("--output", "output_path", type=click.Path(path_type=Path), default=None,
              help="Output directory [default: current directory]")
@click.option("--output-name", default=None,
              help="Override output filename root [default: input file stem]")
@click.option("--stopwords", "stopwords_path",
              type=click.Path(exists=True, path_type=Path), default=None,
              help="Stopword list file; one word per line")
@click.option("--top-n", default=100, type=int, show_default=True,
              help="Words per POS list")
@click.option("--pos", default=None,
              help="Comma-separated POS filter e.g. noun,adjective")
@click.option("--ranker", "ranker_name", default="distinctive", show_default=True,
              help="Ranking strategy: frequency | distinctive")
@click.option("--split", is_flag=True, default=False,
              help="Write one file per POS instead of combined")
@click.option("--html-report", is_flag=True, default=False,
              help="Also generate HTML ranker report")
def cli(input_file, output_path, output_name, stopwords_path, top_n, pos, ranker_name, split, html_report):
    """Generate thematic word frequency tables from source texts."""
    try:
        ranker = ranker_for(ranker_name)
    except ValueError as e:
        raise click.BadParameter(str(e), param_hint="--ranker")

    pos_filter = None
    if pos is not None:
        pos_filter = set()
        for name in pos.split(","):
            name = name.strip().lower()
            if name not in _POS_NAMES:
                valid = ", ".join(sorted(_POS_NAMES))
                raise click.BadParameter(
                    f"Unknown POS '{name}'. Valid options: {valid}",
                    param_hint="--pos",
                )
            pos_filter.add(_POS_NAMES[name])

    out_dir = output_path if output_path is not None else Path(".")
    stem = output_name if output_name is not None else input_file.stem
    md_path = out_dir / f"{stem}.md"
    html_path = out_dir / f"{stem}-report.html"

    text = reader_for(input_file).read()
    tokens = nlp_pipeline.process(text)
    counts = counter.count(tokens)
    counts = _filter.apply_stopwords(counts, stopwords_path)

    if pos_filter is not None:
        counts = {p: lemmas for p, lemmas in counts.items() if p in pos_filter}

    ranked = {
        p: ranker.rank(lemmas, top_n)
        for p, lemmas in counts.items()
        if lemmas
    }

    MarkdownWriter().write(ranked, md_path, split=split)

    if html_report:
        html_reporter.render(counts, ranked, html_path, ranker_name=ranker_name)
