import json
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class Rule:
    rule_id: str
    salience: int
    when: Dict[str, Any]
    then: List[Dict[str, Any]]


@dataclass(frozen=True)
class Question:
    fact: str
    qtype: str
    prompt: str


class KnowledgeBase:
    """Loads questions and production rules from JSON files."""

    def __init__(self, questions: List[Question], rules: List[Rule]) -> None:
        self.questions = questions
        self.rules = rules

    @classmethod
    def from_files(cls, questions_path: str, rules_path: str) -> "KnowledgeBase":
        with open(questions_path, "r", encoding="utf-8") as handle:
            questions_raw = json.load(handle)
        with open(rules_path, "r", encoding="utf-8") as handle:
            rules_raw = json.load(handle)

        questions = [
            Question(fact=q["fact"], qtype=q["type"], prompt=q["prompt"])
            for q in questions_raw.get("questions", [])
        ]
        rules = [
            Rule(
                rule_id=r["id"],
                salience=int(r.get("salience", 0)),
                when=r["when"],
                then=r.get("then", []),
            )
            for r in rules_raw.get("rules", [])
        ]
        return cls(questions=questions, rules=rules)
