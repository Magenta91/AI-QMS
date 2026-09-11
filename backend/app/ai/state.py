from typing import Any, TypedDict

class ComplaintGraphState(TypedDict, total=False):
    raw_input: str
    source_type: str
    extracted_text: str
    complaint: dict[str, Any]
    missing_fields: list[str]
    validation_errors: list[str]
    completeness: float
    risk_assessment: dict[str, Any]
    user_correction: dict[str, Any]
    copilot_response: str
    error: str
