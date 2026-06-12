from click.testing import CliRunner

from book_munger.cli import cli


def test_help_exits_cleanly():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output
