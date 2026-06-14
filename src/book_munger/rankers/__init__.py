from .base import BaseRanker
from .distinctive import DistinctivenessRanker
from .frequency import FrequencyRanker

_RANKERS: dict[str, type[BaseRanker]] = {
    "frequency": FrequencyRanker,
    "distinctive": DistinctivenessRanker,
}


def ranker_for(name: str) -> BaseRanker:
    if name not in _RANKERS:
        valid = ", ".join(sorted(_RANKERS))
        raise ValueError(f"Unknown ranker '{name}'. Valid options: {valid}")
    return _RANKERS[name]()
