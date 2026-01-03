from dataclasses import dataclass
from typing import List

from es.knowledge_base import Rule
from es.working_memory import WorkingMemory


@dataclass(frozen=True)
class Activation:
    """Описывает активированное правило с расчетными метриками."""

    rule: Rule
    specificity: int
    recency: int


class ConflictResolver:
    """Разрешает конфликты между активированными правилами по стратегии."""

    def __init__(self, strategy: str) -> None:
        """Сохраняет выбранную стратегию разрешения конфликтов."""
        self.strategy = strategy

    def choose(self, activations: List[Activation]) -> Activation:
        """Выбирает одно правило на основе текущей стратегии."""
        if not activations:
            raise ValueError("No activations to resolve")

        if self.strategy == "salience":
            return max(activations, key=lambda a: a.rule.salience)
        if self.strategy == "specificity":
            return max(activations, key=lambda a: a.specificity)
        if self.strategy == "recency":
            return max(activations, key=lambda a: a.recency)

        if self.strategy == "salience_specificity":
            return max(
                activations,
                key=lambda a: (a.rule.salience, a.specificity, a.recency),
            )
        if self.strategy == "specificity_recency":
            return max(
                activations,
                key=lambda a: (a.specificity, a.recency, a.rule.salience),
            )

        raise ValueError(f"Unknown strategy: {self.strategy}")


def build_activation(rule: Rule, wm: WorkingMemory, specificity: int, fact_names: List[str]) -> Activation:
    """Формирует активирование и вычисляет новизну по фактам условий."""
    recency = max((wm.timestamp(name) for name in fact_names), default=0)
    return Activation(rule=rule, specificity=specificity, recency=recency)
