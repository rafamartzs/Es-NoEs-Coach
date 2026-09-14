from typing import Literal
from pydantic import BaseModel, Field


FieldStatus = Literal["known", "verify", "pending", "not_applicable"]
ContrastQuality = Literal["excellent", "useful", "weak", "invalid", "not_evaluable"]


class InvestigationAction(BaseModel):
    action: str = Field(description="Concrete action to obtain or verify missing information.")
    evidence_expected: str = Field(description="What evidence or result this action should produce.")


class EvaluationResult(BaseModel):
    status: FieldStatus = Field(
        description="State of the information: known, verify, pending, or not_applicable."
    )
    contrast_quality: ContrastQuality = Field(
        description="Methodological quality of the proposed IS / IS-NOT contrast."
    )
    answer_summary: str = Field(
        description="Short factual summary of what is currently known."
    )
    primary_contrast: str = Field(
        description="Best current IS / IS-NOT comparison. If not yet known, say what is missing."
    )
    secondary_contrasts: list[str] = Field(
        description="Useful secondary or exploratory comparisons that should not replace the primary contrast."
    )
    relevant_differences: list[str] = Field(
        description="Observed differences only. Do not infer root cause."
    )
    missing_information: list[str] = Field(
        description="Important information that is still unknown or unverified."
    )
    suggested_actions: list[InvestigationAction] = Field(
        description="Practical ways to obtain or verify missing information."
    )
    next_question: str = Field(
        description="The single best follow-up question to ask the engineer next."
    )
    methodological_warning: str = Field(
        description="Any key methodological warning, or 'None' if there is no warning."
    )
    causal_boundary_note: str = Field(
        description="Reminder that differences are clues, not demonstrated causes."
    )
