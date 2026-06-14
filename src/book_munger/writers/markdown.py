from pathlib import Path

from .base import BaseWriter

_POS_LABELS = {
    "NOUN": "Nouns",
    "VERB": "Verbs",
    "ADJ": "Adjectives",
    "ADV": "Adverbs",
}


def _pos_label(pos: str) -> str:
    return _POS_LABELS.get(pos, pos.title())


class MarkdownWriter(BaseWriter):
    def write(self, ranked: dict[str, list[str]], path: Path, split: bool = False) -> None:
        if split:
            self._write_split(ranked, path)
        else:
            self._write_combined(ranked, path)

    def _write_combined(self, ranked: dict[str, list[str]], path: Path) -> None:
        if not ranked:
            path.write_text("", encoding="utf-8")
            return

        headers = [_pos_label(pos) for pos in ranked]
        columns = list(ranked.values())
        max_rows = max(len(col) for col in columns)

        header_row = "| " + " | ".join(headers) + " |"
        sep_row = "| " + " | ".join("---" for _ in headers) + " |"

        rows = [header_row, sep_row]
        for i in range(max_rows):
            cells = [col[i] if i < len(col) else "" for col in columns]
            rows.append("| " + " | ".join(cells) + " |")

        path.write_text("\n".join(rows) + "\n", encoding="utf-8")

    def _write_split(self, ranked: dict[str, list[str]], path: Path) -> None:
        stem = path.stem
        parent = path.parent
        for pos, words in ranked.items():
            label = _pos_label(pos)
            out = parent / f"{stem}-{label.lower()}.md"
            lines = [f"# {label} ({len(words)} words)"] + words
            out.write_text("\n".join(lines) + "\n", encoding="utf-8")
