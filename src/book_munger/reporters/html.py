from pathlib import Path

from jinja2 import Environment, FileSystemLoader

_TEMPLATE_DIR = Path(__file__).parent / "templates"


def render(
    counts: dict[str, dict[str, int]],
    ranked: dict[str, list[str]],
    output_path: Path,
    ranker_name: str = "",
) -> None:
    total_tokens = sum(sum(pos_counts.values()) for pos_counts in counts.values())
    vocab_size = sum(len(pos_counts) for pos_counts in counts.values())
    pos_breakdown = [
        (pos, len(counts[pos]), sum(counts[pos].values()))
        for pos in ranked
        if pos in counts
    ]

    env = Environment(loader=FileSystemLoader(str(_TEMPLATE_DIR)), autoescape=True)
    template = env.get_template("report.html.j2")
    html = template.render(
        ranker_name=ranker_name,
        total_tokens=total_tokens,
        vocab_size=vocab_size,
        pos_breakdown=pos_breakdown,
        ranked=ranked,
        counts=counts,
    )
    output_path.write_text(html, encoding="utf-8")
