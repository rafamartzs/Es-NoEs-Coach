from coach_agent import evaluate_case
from question_specs import QUESTION_SPECS


def ask(prompt: str, allow_blank: bool = True) -> str:
    while True:
        value = input(prompt).strip()
        if value or allow_blank:
            return value
        print("Please enter a value.")


def print_questions() -> None:
    print("\nAvailable questions:\n")
    for qid, spec in QUESTION_SPECS.items():
        print(f"{qid:>2}. [{spec['dimension']}] {spec['name']}")


def print_result(result) -> None:
    print("\n" + "=" * 72)
    print("EVALUATION")
    print("=" * 72)
    print(f"Status:            {result.status}")
    print(f"Contrast quality:  {result.contrast_quality}")
    print(f"Summary:           {result.answer_summary}")
    print(f"Primary contrast:  {result.primary_contrast}")

    if result.secondary_contrasts:
        print("\nSecondary / exploratory contrasts:")
        for item in result.secondary_contrasts:
            print(f"  - {item}")

    if result.relevant_differences:
        print("\nRelevant differences observed:")
        for item in result.relevant_differences:
            print(f"  - {item}")

    if result.missing_information:
        print("\nMissing / unverified information:")
        for item in result.missing_information:
            print(f"  - {item}")

    if result.suggested_actions:
        print("\nSuggested investigation actions:")
        for item in result.suggested_actions:
            print(f"  - {item.action}")
            print(f"    Evidence expected: {item.evidence_expected}")

    print(f"\nNext question: {result.next_question}")
    print(f"Method warning: {result.methodological_warning}")
    print(f"Causal boundary: {result.causal_boundary_note}")
    print("=" * 72)


def main() -> None:
    print("\nProblem Solving Coach - Console MVP v0.1")
    print("This prototype evaluates one IS / IS-NOT field at a time.")

    print_questions()

    while True:
        try:
            question_id = int(ask("\nQuestion number (1-13): ", allow_blank=False))
            if question_id not in QUESTION_SPECS:
                raise ValueError
            break
        except ValueError:
            print("Choose a number from 1 to 13.")

    spec = QUESTION_SPECS[question_id]
    print(f"\nSelected: {spec['name']}")
    print(f"Objective: {spec['objective']}\n")

    problem = ask("Problem statement: ")
    defect = ask("Defect / failure mode: ")
    is_value = ask("IS: ")
    is_not_value = ask("IS-NOT (you may write 'unknown'): ")
    difference = ask("Known difference (blank/unknown is valid): ")
    context = ask("Additional context: ")

    print("\nEvaluating...\n")
    result = evaluate_case(
        question_id=question_id,
        problem_statement=problem,
        defect_mode=defect,
        is_value=is_value,
        is_not_value=is_not_value,
        known_difference=difference,
        context=context,
    )
    print_result(result)


if __name__ == "__main__":
    main()
