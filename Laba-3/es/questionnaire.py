from typing import Any, List

from es.knowledge_base import Question
from es.working_memory import WorkingMemory


class Questionnaire:
    """Опрос пользователя и запись исходных фактов."""

    def __init__(self, questions: List[Question], wm: WorkingMemory) -> None:
        """Сохраняет список вопросов и рабочую память."""
        self._questions = questions
        self._wm = wm

    def conduct(self) -> None:
        """Проходит по вопросам и сохраняет ответы как факты."""
        for question in self._questions:
            value = self._ask(question)
            self._wm.assert_fact(question.fact, value, None)

    def _ask(self, question: Question) -> Any:
        """Запрашивает ответ, пока он не соответствует типу вопроса."""
        while True:
            raw = input(question.prompt).strip().lower()
            if question.qtype == "int":
                if raw.lstrip("-").isdigit():
                    return int(raw)
                print("Ошибка: ожидается целое число.")
                continue

            if question.qtype == "bool":
                if raw in {"yes", "y"}:
                    return "yes"
                if raw in {"no", "n"}:
                    return "no"
                print("Введите 'yes' или 'no'.")
                continue

            return raw
