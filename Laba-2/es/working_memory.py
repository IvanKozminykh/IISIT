from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class FactSource:
    rule_id: str
    premises: List[str]


class WorkingMemory:
    """Stores facts, their timestamps, and provenance for explanations."""

    def __init__(self) -> None:
        self._facts: Dict[str, Any] = {}
        self._timestamps: Dict[str, int] = {}
        self._sources: Dict[str, FactSource] = {}
        self._counter = 0

    def assert_fact(self, name: str, value: Any, source: Optional[FactSource]) -> bool:
        existing = self._facts.get(name)
        if existing == value:
            return False

        self._facts[name] = value
        self._counter += 1
        self._timestamps[name] = self._counter
        if source is not None:
            self._sources[name] = source
        return True

    def get_fact(self, name: str) -> Optional[Any]:
        return self._facts.get(name)

    def has_fact(self, name: str) -> bool:
        return name in self._facts

    def timestamp(self, name: str) -> int:
        return self._timestamps.get(name, 0)

    def facts(self) -> Dict[str, Any]:
        return dict(self._facts)

    def source(self, name: str) -> Optional[FactSource]:
        return self._sources.get(name)
