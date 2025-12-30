from pathlib import Path

from es.conflict_resolution import ConflictResolver
from es.explanation import Explanation
from es.knowledge_base import KnowledgeBase
from es.questionnaire import Questionnaire
from es.rule_engine import RuleEngine
from es.semantic_matcher import SemanticMatcher
from es.semantic_network import SemanticNetwork
from es.working_memory import WorkingMemory


def choose_strategy() -> str:
    strategies = {
        "1": ("salience", "Приоритет по salience"),
        "2": ("specificity", "Приоритет по количеству условий"),
        "3": ("recency", "Приоритет по новизне фактов"),
        "4": ("salience_specificity", "Salience -> специфичность -> новизна"),
        "5": ("specificity_recency", "Специфичность -> новизна -> salience"),
    }

    print("Выберите стратегию разрешения конфликтов для правил:")
    for key, (_, label) in strategies.items():
        print(f"  {key}) {label}")

    while True:
        choice = input("Номер стратегии: ").strip()
        if choice in strategies:
            return strategies[choice][0]
        print("Некорректный выбор. Попробуйте снова.")


def run_queries(network: SemanticNetwork, explainer: Explanation) -> None:
    print("\nЗапросы к семантической сети:")
    print("  1) is-a (является ли A подтипом B)")
    print("  2) has-relation (есть ли отношение A -R-> B)")
    print("  3) path (путь между A и B)")
    print("  4) завершить")

    while True:
        choice = input("Номер запроса: ").strip()
        if choice == "4":
            break
        if choice == "1":
            source = input("A: ").strip()
            target = input("B: ").strip()
            result = network.is_a(source, target)
            print(f"Результат: {result}")
            continue
        if choice == "2":
            source = input("A: ").strip()
            relation = input("Отношение R: ").strip()
            target = input("B: ").strip()
            result = network.has_relation(source, relation, target)
            print(f"Результат: {result}")
            continue
        if choice == "3":
            source = input("A: ").strip()
            target = input("B: ").strip()
            path = explainer.explain_path(network, source, target)
            if path:
                print(f"Путь: {path}")
            else:
                print("Путь не найден.")
            continue
        print("Некорректный выбор. Попробуйте снова.")


def main() -> None:
    base_path = Path(__file__).parent
    kb = KnowledgeBase.from_files(
        str(base_path / "kb" / "questions.json"),
        str(base_path / "kb" / "rules.json"),
    )
    network = SemanticNetwork.from_json(str(base_path / "kb" / "semantic_network.json"))

    wm = WorkingMemory()
    questionnaire = Questionnaire(kb.questions, wm)
    questionnaire.conduct()

    strategy = choose_strategy()
    resolver = ConflictResolver(strategy)
    rule_engine = RuleEngine(kb.rules, resolver, wm)
    rule_engine.run()

    matcher = SemanticMatcher(network)
    result = matcher.recommend(wm)
    if result:
        matcher.assert_recommendation(wm, result)
        print(f"\nРекомендация: {result.recommendation}")
    else:
        print("\nРекомендация не найдена. Проверьте вводимые данные.")

    if result:
        print("\nОбъяснение:")
        explainer = Explanation(wm)
        for line in explainer.explain_fact("recommendation"):
            print(line)

    if input("\nВыполнить запросы к БЗ? (yes/no): ").strip().lower() in {"yes", "y"}:
        explainer = Explanation(wm)
        run_queries(network, explainer)


if __name__ == "__main__":
    main()
