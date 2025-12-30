from pathlib import Path

from es.conflict_resolution import ConflictResolver
from es.explanation import Explanation
from es.inference_engine import InferenceEngine
from es.knowledge_base import KnowledgeBase
from es.questionnaire import Questionnaire
from es.working_memory import WorkingMemory


def choose_strategy() -> str:
    strategies = {
        "1": ("salience", "Приоритет по salience"),
        "2": ("specificity", "Приоритет по количеству условий"),
        "3": ("recency", "Приоритет по новизне фактов"),
        "4": ("salience_specificity", "Salience -> специфичность -> новизна"),
        "5": ("specificity_recency", "Специфичность -> новизна -> salience"),
    }

    print("Выберите стратегию разрешения конфликтов:")
    for key, (_, label) in strategies.items():
        print(f"  {key}) {label}")

    while True:
        choice = input("Номер стратегии: ").strip()
        if choice in strategies:
            return strategies[choice][0]
        print("Некорректный выбор. Попробуйте снова.")


def main() -> None:
    kb_path = Path(__file__).parent / "kb" / "knowledge_base.json"
    kb = KnowledgeBase.from_json(str(kb_path))

    wm = WorkingMemory()
    wm.assert_fact("recommendation-made", "no", None)

    questionnaire = Questionnaire(kb.questions, wm)
    questionnaire.conduct()

    strategy = choose_strategy()
    resolver = ConflictResolver(strategy)
    engine = InferenceEngine(kb.rules, resolver, wm)
    engine.run()

    recommendation = wm.get_fact("recommendation")
    if recommendation:
        print(f"\nРекомендация: {recommendation}")
    else:
        print("\nРекомендация не найдена. Проверьте вводимые данные.")

    if recommendation:
        print("\nОбъяснение:")
        explainer = Explanation(wm)
        for line in explainer.explain_fact("recommendation"):
            print(line)


if __name__ == "__main__":
    main()
