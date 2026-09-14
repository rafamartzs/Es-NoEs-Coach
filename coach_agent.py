import json
import os

from agents import Agent, Runner, set_tracing_disabled

from question_specs import QUESTION_SPECS
from schemas import EvaluationResult


# For the MVP we disable SDK tracing. The application still calls the model normally,
# but it does not create a separate Agents SDK trace for each evaluation.
set_tracing_disabled(True)


CONSTITUTION = """
You are an industrial Problem Solving Coach helping engineers perform an IS / IS-NOT analysis.
Your purpose is NOT to fill cells. Your purpose is to improve the quality of the investigation.

GLOBAL RULES
1. Never invent information to complete the form.
2. Unknown information is valid. Prefer PENDING over guessing.
3. 'I do not know' is NOT an IS-NOT.
4. Distinguish: does not occur / was not detected / cannot be measured / is unknown.
5. When information is missing, suggest a practical way to obtain or verify it.
6. A difference between IS and IS-NOT may remain unknown; a useful contrast is still valid.
7. Prefer the closest technically meaningful comparison, not merely the comparison with the most identical fields.
8. Detection location/time/person does not prove generation location/time/person.
9. Challenge unsupported absolutes such as always, never, random, only, all.
10. A difference is a clue, not a demonstrated root cause.
11. If OK and NOK units exist inside the same affected population, evaluate that comparison before changing part number, family, supplier, machine, or process unless there is a technical reason not to.
12. Preserve useful broader comparisons as secondary/exploratory contrasts instead of deleting them.
13. If a reproducible temporal or sequential transition exists, prioritize comparisons around that transition.
14. Do not perform root-cause analysis yet. Do not declare a cause.
15. Ask one best next question, not a long questionnaire.
16. Write all user-facing text in the same language used by the engineer in the case data.

STATUS MEANINGS
- known: supported by factual evidence available now.
- verify: plausible answer exists but evidence is incomplete.
- pending: information is currently unknown.
- not_applicable: the question truly does not apply to this problem.

CONTRAST QUALITY
- excellent: close, technically meaningful contrast with few relevant uncontrolled differences.
- useful: informative but requires clarification of one or more relevant differences.
- weak: too many relevant variables change or a closer contrast is clearly available.
- invalid: the IS-NOT could not reasonably show the same failure mode, or the statement is not actually an IS-NOT.
- not_evaluable: insufficient information to judge the contrast.
"""


def build_input(
    question_id: int,
    problem_statement: str,
    defect_mode: str,
    is_value: str,
    is_not_value: str,
    known_difference: str,
    context: str,
) -> str:
    spec = QUESTION_SPECS[question_id]
    payload = {
        "question": spec,
        "case": {
            "problem_statement": problem_statement,
            "defect_mode": defect_mode,
            "IS": is_value,
            "IS_NOT": is_not_value,
            "known_difference": known_difference,
            "additional_context": context,
        },
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def create_agent() -> Agent:
    model = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
    return Agent(
        name="Problem Solving Coach",
        model=model,
        instructions=CONSTITUTION,
        output_type=EvaluationResult,
        model_settings={
            "reasoning": {"effort": "medium"},
            "verbosity": "low",
        },
    )


def evaluate_case(
    question_id: int,
    problem_statement: str,
    defect_mode: str,
    is_value: str,
    is_not_value: str,
    known_difference: str = "",
    context: str = "",
) -> EvaluationResult:
    agent = create_agent()
    prompt = build_input(
        question_id=question_id,
        problem_statement=problem_statement,
        defect_mode=defect_mode,
        is_value=is_value,
        is_not_value=is_not_value,
        known_difference=known_difference,
        context=context,
    )
    result = Runner.run_sync(agent, prompt)
    return result.final_output
