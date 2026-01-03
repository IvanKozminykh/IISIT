from typing import List, Set

from es.working_memory import WorkingMemory


class Explanation:
    """Строит цепочки объяснения по источникам фактов."""

    def __init__(self, wm: WorkingMemory) -> None:
        """Сохраняет рабочую память для построения объяснений."""
        self._wm = wm

    def explain_fact(self, fact: str) -> List[str]:
        """Возвращает список строк объяснения для выбранного факта."""
        lines: List[str] = []
        self._build_chain(fact, lines, set(), 0)
        return lines

    def _build_chain(self, fact: str, lines: List[str], visited: Set[str], depth: int) -> None:
        """Рекурсивно раскрывает предпосылки и строит дерево объяснения."""
        if fact in visited:
            return
        visited.add(fact)

        value = self._wm.get_fact(fact)
        indent = "  " * depth
        source = self._wm.source(fact)

        if source is None:
            lines.append(f"{indent}- {fact} = {value} (исходный факт)")
            return

        lines.append(f"{indent}- {fact} = {value} (правило {source.rule_id})")
        for premise in source.premises:
            name = premise.split("=")[0]
            self._build_chain(name, lines, visited, depth + 1)
