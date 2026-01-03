from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class FactSource:
    """Описывает источник факта: правило и предпосылки."""

    rule_id: str
    premises: List[str]


class WorkingMemory:
    """Хранит факты, временные метки и источник для объяснений."""

    def __init__(self) -> None:
        """Инициализирует пустую рабочую память и счетчик времени."""
        self._facts: Dict[str, Any] = {}
        self._timestamps: Dict[str, int] = {}
        self._sources: Dict[str, FactSource] = {}
        self._counter = 0

    def assert_fact(self, name: str, value: Any, source: Optional[FactSource]) -> bool:
        """Добавляет/обновляет факт и фиксирует время/источник."""
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
        """Возвращает значение факта, если он существует."""
        return self._facts.get(name)

    def has_fact(self, name: str) -> bool:
        """Проверяет наличие факта в рабочей памяти."""
        return name in self._facts

    def timestamp(self, name: str) -> int:
        """Возвращает метку времени для стратегии новизны."""
        return self._timestamps.get(name, 0)

    def facts(self) -> Dict[str, Any]:
        """Возвращает копию всех фактов."""
        return dict(self._facts)

    def source(self, name: str) -> Optional[FactSource]:
        """Возвращает источник факта, если он был выведен."""
        return self._sources.get(name)
