from typing import List, Optional, Set

from es.semantic_network import SemanticNetwork
from es.working_memory import WorkingMemory


class Explanation:
    """Generates explanation chains from working memory and network paths."""

    def __init__(self, wm: WorkingMemory) -> None:
        self._wm = wm

    def explain_fact(self, fact: str) -> List[str]:
        lines: List[str] = []
        self._build_chain(fact, lines, set(), 0)
        return lines

    def explain_path(self, network: SemanticNetwork, source: str, target: str) -> Optional[str]:
        path = network.find_path(source, target)
        if not path:
            return None
        return " -> ".join(path)

    def _build_chain(self, fact: str, lines: List[str], visited: Set[str], depth: int) -> None:
        if fact in visited:
            return
        visited.add(fact)

        value = self._wm.get_fact(fact)
        indent = "  " * depth
        source = self._wm.source(fact)

        if source is None:
            lines.append(f"{indent}- {fact} = {value} (исходный факт)")
            return

        lines.append(f"{indent}- {fact} = {value} (источник {source.rule_id})")
        for premise in source.premises:
            name = premise.split("=")[0]
            self._build_chain(name, lines, visited, depth + 1)
