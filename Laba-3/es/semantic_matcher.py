from dataclasses import dataclass
from typing import List, Optional, Set

from es.semantic_network import SemanticNetwork
from es.working_memory import FactSource, WorkingMemory


@dataclass(frozen=True)
class MatchResult:
    """Результат сопоставления признаков и рекомендация GPU."""
    recommendation: str
    matched_features: List[str]


class SemanticMatcher:
    """Сопоставляет выведенные признаки с GPU-узлами в сети."""

    def __init__(self, network: SemanticNetwork) -> None:
        """Сохраняет семантическую сеть для поиска рекомендаций."""
        self._network = network

    def recommend(self, wm: WorkingMemory) -> Optional[MatchResult]:
        """Возвращает рекомендацию GPU на основе активных признаков."""
        active_features = self._collect_active_features(wm)
        candidates = []
        for gpu in self._network.nodes_by_type("gpu"):
            required = self._required_features(gpu.node_id)
            if required and not required.issubset(active_features):
                continue
            candidates.append((gpu.rank or 999, gpu.node_id, sorted(required)))

        if not candidates:
            return None

        candidates.sort(key=lambda item: (item[0], -len(item[2])))
        _, gpu_id, matched = candidates[0]
        return MatchResult(recommendation=gpu_id, matched_features=matched)

    def assert_recommendation(self, wm: WorkingMemory, result: MatchResult) -> None:
        """Записывает рекомендацию в рабочую память как выведенный факт."""
        premises = [f"{name}=yes" for name in result.matched_features]
        source = FactSource(rule_id="semantic-match", premises=premises)
        wm.assert_fact("recommendation", result.recommendation, source)

    def _required_features(self, gpu_id: str) -> Set[str]:
        """Возвращает набор признаков, требуемых для GPU-узла."""
        edges = self._network.edges_from(gpu_id, "has-feature")
        return {edge.target for edge in edges}

    @staticmethod
    def _collect_active_features(wm: WorkingMemory) -> Set[str]:
        """Собирает признаки со значением yes из рабочей памяти."""
        return {name for name, value in wm.facts().items() if value == "yes"}
