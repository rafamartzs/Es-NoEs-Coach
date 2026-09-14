from coach_agent import evaluate_case
from example_cases import EXAMPLES


for case in EXAMPLES:
    print("\n" + "#" * 80)
    print(case["name"])
    print("#" * 80)
    result = evaluate_case(
        question_id=case["question_id"],
        problem_statement=case["problem_statement"],
        defect_mode=case["defect_mode"],
        is_value=case["is_value"],
        is_not_value=case["is_not_value"],
        known_difference=case["known_difference"],
        context=case["context"],
    )
    print(result.model_dump_json(indent=2))
