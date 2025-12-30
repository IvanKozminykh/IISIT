from typing import Any, Dict, List, Set

from es.conflict_resolution import ConflictResolver, build_activation
from es.knowledge_base import Rule
from es.working_memory import FactSource, WorkingMemory


class RuleEngine:
    """Forward chaining inference engine for production rules."""

    def __init__(self, rules: List[Rule], resolver: ConflictResolver, wm: WorkingMemory) -> None:
        self._rules = rules
        self._resolver = resolver
        self._wm = wm
        self.fired_rules: List[str] = []
        self._fired_set: Set[str] = set()

    def run(self, max_steps: int = 100) -> None:
        steps = 0
        while steps < max_steps:
            activations = []
            for rule in self._rules:
                if rule.rule_id in self._fired_set:
                    continue
                if self._evaluate(rule.when):
                    fact_names = self._collect_fact_names(rule.when)
                    specificity = len(fact_names)
                    activations.append(build_activation(rule, self._wm, specificity, fact_names))

            if not activations:
                break

            activation = self._resolver.choose(activations)
            self._fire(activation.rule)
            steps += 1

    def _fire(self, rule: Rule) -> None:
        fact_names = self._collect_fact_names(rule.when)
        premises = [f"{name}={self._wm.get_fact(name)}" for name in fact_names]
        source = FactSource(rule_id=rule.rule_id, premises=premises)

        for action in rule.then:
            assertion = action.get("assert")
            if assertion:
                name = assertion["fact"]
                value = assertion["value"]
                self._wm.assert_fact(name, value, source)

        self._fired_set.add(rule.rule_id)
        self.fired_rules.append(rule.rule_id)

    def _evaluate(self, expr: Dict[str, Any]) -> bool:
        if "all" in expr:
            return all(self._evaluate(item) for item in expr["all"])
        if "any" in expr:
            return any(self._evaluate(item) for item in expr["any"])

        fact = expr.get("fact")
        op = expr.get("op")
        value = expr.get("value")
        if fact is None or op is None:
            return False

        fact_value = self._wm.get_fact(fact)
        if fact_value is None:
            return False

        return self._compare(fact_value, op, value)

    @staticmethod
    def _compare(left: Any, op: str, right: Any) -> bool:
        if op == "==":
            return left == right
        if op == "!=":
            return left != right
        if op == ">":
            return left > right
        if op == ">=":
            return left >= right
        if op == "<":
            return left < right
        if op == "<=":
            return left <= right
        raise ValueError(f"Unsupported operator: {op}")

    def _collect_fact_names(self, expr: Dict[str, Any]) -> List[str]:
        if "all" in expr:
            names = []
            for item in expr["all"]:
                names.extend(self._collect_fact_names(item))
            return self._dedupe(names)
        if "any" in expr:
            names = []
            for item in expr["any"]:
                names.extend(self._collect_fact_names(item))
            return self._dedupe(names)

        fact = expr.get("fact")
        return [fact] if fact else []

    @staticmethod
    def _dedupe(names: List[str]) -> List[str]:
        seen = set()
        result = []
        for name in names:
            if name not in seen:
                seen.add(name)
                result.append(name)
        return result
