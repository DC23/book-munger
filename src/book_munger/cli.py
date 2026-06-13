from pathlib import Path

import click

from book_munger.readers import reader_for


@click.group()
def cli():
    """Generate thematic word frequency tables from source texts."""


@cli.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
def process(input_file):
    """Process a book and print its cleaned text."""
    reader = reader_for(input_file)
    text = reader.read()
    click.echo(text)
