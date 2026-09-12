from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class Complaint(BaseModel):
    complaint_source: str | None = None
    customer_name: str | None = None
    product_name: str | None = None
    product_strength: str | None = None
    batch_number: str | None = None
    affected_quantity: str | None = None
    manufacturing_date: str | None = None
    expiry_date: str | None = None
    complaint_date: str | None = None
    originating_site: str | None = None
    affected_material: str | None = None
    complaint_type: str | None = None
    complaint_description: str | None = None
    initial_severity: str | None = None
    priority: str | None = None

class ComplaintTextRequest(BaseModel):
    text: str = Field(min_length=1)

class ComplaintProcessRequest(BaseModel):
    text: str = Field(min_length=1)
    source_type: str = Field(default="text")

class ComplaintCorrectRequest(BaseModel):
    complaint_data: Dict[str, Any]
    user_message: str
    field: Optional[str] = None

class ComplaintResponse(BaseModel):
    id: Optional[int] = None
    complaint: Complaint
    completeness: Optional[float] = None
    missing_fields: Optional[List[str]] = None
    validation_errors: Optional[List[str]] = None
    risk_assessment: Optional[Dict[str, Any]] = None

class RiskAssessment(BaseModel):
    risk_level: str
    reasons: List[str]
    recommended_action: str
    confidence: Optional[float] = None
