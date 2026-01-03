import json
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Node:
    """Узел семантической сети."""
    node_id: str
    node_type: str
    label: str
    rank: Optional[int] = None


@dataclass(frozen=True)
class Edge:
    """Дуга семантической сети с типом отношения."""
    source: str
    target: str
    relation: str


class SemanticNetwork:
    """Семантическая сеть с узлами, отношениями и запросами."""

    def __init__(self, nodes: Dict[str, Node], edges: List[Edge]) -> None:
        """Сохраняет узлы/дуги и строит индекс исходящих связей."""
        self._nodes = nodes
        self._edges = edges
        self._outgoing: Dict[str, List[Edge]] = {}
        for edge in edges:
            self._outgoing.setdefault(edge.source, []).append(edge)

    @classmethod
    def from_json(cls, path: str) -> "SemanticNetwork":
        """Загружает семантическую сеть из JSON-файла."""
        with open(path, "r", encoding="utf-8") as handle:
            raw = json.load(handle)

        nodes = {}
        for item in raw.get("nodes", []):
            nodes[item["id"]] = Node(
                node_id=item["id"],
                node_type=item.get("type", ""),
                label=item.get("label", item["id"]),
                rank=item.get("rank"),
            )
        edges = [
            Edge(source=e["from"], target=e["to"], relation=e["relation"])
            for e in raw.get("edges", [])
        ]
        return cls(nodes=nodes, edges=edges)

    def node(self, node_id: str) -> Optional[Node]:
        """Возвращает узел по идентификатору."""
        return self._nodes.get(node_id)

    def nodes_by_type(self, node_type: str) -> List[Node]:
        """Возвращает список узлов заданного типа."""
        return [n for n in self._nodes.values() if n.node_type == node_type]

    def edges_from(self, node_id: str, relation: Optional[str] = None) -> List[Edge]:
        """Возвращает исходящие дуги узла (опционально по типу отношения)."""
        edges = self._outgoing.get(node_id, [])
        if relation is None:
            return list(edges)
        return [edge for edge in edges if edge.relation == relation]

    def has_relation(self, source: str, relation: str, target: str) -> bool:
        """Проверяет наличие отношения source -relation-> target."""
        return any(
            edge.relation == relation and edge.target == target
            for edge in self.edges_from(source, relation)
        )

    def is_a(self, source: str, target: str) -> bool:
        """Проверяет, является ли source подтипом target (транзитивно)."""
        if source == target:
            return True
        visited = set()
        queue = [source]
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            for edge in self.edges_from(current, "is-a"):
                if edge.target == target:
                    return True
                queue.append(edge.target)
        return False

    def find_path(self, source: str, target: str, max_depth: int = 4) -> Optional[List[str]]:
        """Ищет путь от source к target в пределах глубины."""
        if source == target:
            return [source]
        queue = [(source, [source])]
        visited = {source}
        while queue:
            current, path = queue.pop(0)
            if len(path) > max_depth:
                continue
            for edge in self.edges_from(current):
                next_node = edge.target
                if next_node == target:
                    return path + [next_node]
                if next_node not in visited:
                    visited.add(next_node)
                    queue.append((next_node, path + [next_node]))
        return None
