import json
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class Rule:
    """Представляет продукционное правило, загруженное из JSON."""

    rule_id: str
    salience: int
    when: Dict[str, Any]
    then: List[Dict[str, Any]]


@dataclass(frozen=True)
class Question:
    """Представляет вопрос пользователю для получения исходного факта."""

    fact: str
    qtype: str
    prompt: str


class KnowledgeBase:
    """Загружает и хранит правила и вопросы в нейтральной структуре."""

    def __init__(self, questions: List[Question], rules: List[Rule]) -> None:
        """Сохраняет уже разобранные вопросы и правила."""
        self.questions = questions
        self.rules = rules

    @classmethod
    def from_json(cls, path: str) -> "KnowledgeBase":
        """Разбирает JSON-БЗ в объекты Question/Rule."""
        with open(path, "r", encoding="utf-8") as handle:
            raw = json.load(handle)

        # Преобразуем словари вопросов в объекты Question.
        questions = [
            Question(fact=q["fact"], qtype=q["type"], prompt=q["prompt"])
            for q in raw.get("questions", [])
        ]
        # Преобразуем словари правил в объекты Rule с приоритетом и действиями.
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
