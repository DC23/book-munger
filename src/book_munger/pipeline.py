import spacy
from functools import lru_cache
from typing import Iterable

_ALLOWED_POS = frozenset({
    "NOUN", "VERB", "ADJ", "ADV", "PROPN", "PRON",
    "CCONJ", "SCONJ", "ADP", "INTJ",
})


@lru_cache(maxsize=None)
def _load_model(model: str) -> spacy.language.Language:
    return spacy.load(model)


def process(text: str, model: str = "en_core_web_sm") -> Iterable[tuple[str, str]]:
    nlp = _load_model(model)
    doc = nlp(text)
    for token in doc:
        if token.pos_ in _ALLOWED_POS:
            yield (token.lemma_.lower(), token.pos_)
