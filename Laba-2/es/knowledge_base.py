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
    """Loads and stores rules/questions in a neutral structure."""

    def __init__(self, questions: List[Question], rules: List[Rule]) -> None:
        self.questions = questions
        self.rules = rules

    @classmethod
    def from_json(cls, path: str) -> "KnowledgeBase":
        with open(path, "r", encoding="utf-8") as handle:
            raw = json.load(handle)

        questions = [
            Question(fact=q["fact"], qtype=q["type"], prompt=q["prompt"])
            for q in raw.get("questions", [])
        ]
        rules = [
            Rule(
                rule_id=r["id"],
                salience=int(r.get("salience", 0)),
                when=r["when"],
                then=r.get("then", []),
            )
            for r in raw.get("rules", [])
        ]
        return cls(questions=questions, rules=rules)
