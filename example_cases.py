"""Synthetic examples for manual testing.

These are intentionally generic. Replace them with anonymized plant cases when testing.
"""

EXAMPLES = [
    {
        "name": "Different part number proposed as IS-NOT",
        "question_id": 1,
        "problem_statement": "Armature family W3 shows commutator height out of specification.",
        "defect_mode": "Commutator height out of specification",
        "is_value": "W3 part 033 NOK",
        "is_not_value": "W4 part 038 OK",
        "known_difference": "Different family and part number",
        "context": "Same machine, same process parameters. OK pieces of part 033 exist in the same shift.",
    },
    {
        "name": "Sequential transition",
        "question_id": 7,
        "problem_statement": "Some commutators show roughness out of specification after turning.",
        "defect_mode": "Rz out of specification",
        "is_value": "Third part after startup is NOK",
        "is_not_value": "Second part after startup is OK",
        "known_difference": "Unknown",
        "context": "First two parts are repeatedly OK; third part repeatedly NOK; later occurrence appears irregular.",
    },
    {
        "name": "Unknown customer quantity",
        "question_id": 10,
        "problem_statement": "Customer reported defective motors.",
        "defect_mode": "Functional failure",
        "is_value": "Customer complaint exists",
        "is_not_value": "Unknown",
        "known_difference": "Unknown",
        "context": "The customer has not yet reported total inspected quantity or total NOK quantity.",
    },
]
