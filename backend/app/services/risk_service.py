from app.services.base_service import BaseService
from app.clients.groq_client import GroqClient
from typing import Dict, Any
import json

class RiskService(BaseService):
    def __init__(self):
        super().__init__("risk")
        self.groq_client = GroqClient()

    def assess(self, complaint: dict) -> dict:
        text = (complaint.get("complaint_description") or "").lower()
        if any(x in text for x in ("discolor", "contamination", "foreign matter")):
            level = "HIGH"
        elif text:
            level = "MEDIUM"
        else:
            level = "LOW"
        return {
            "risk_level": level,
            "reasons": ["Initial placeholder assessment; replace with AI workflow."],
            "recommended_action": "Human QA review required."
        }

    async def assess_risk(self, complaint_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform AI-assisted risk assessment"""
        self.logger.info("Performing AI risk assessment")
        
        try:
            # Build prompt for risk assessment
            complaint_summary = self._build_complaint_summary(complaint_data)
            
            prompt = f"""You are a pharmaceutical quality assurance AI assistant. Assess the risk level of this customer complaint.

Complaint Details:
{complaint_summary}

Provide a risk assessment with:
1. risk_level: HIGH, MEDIUM, or LOW
2. reasons: List of 2-3 specific reasons for this risk level
3. recommended_action: Specific recommended next steps

Consider factors like:
- Product safety implications
- Potential patient harm
- Regulatory reporting requirements
- Batch disposition needs
- Investigation scope

Respond ONLY with valid JSON in this exact format:
{{
  "risk_level": "HIGH|MEDIUM|LOW",
  "reasons": ["reason 1", "reason 2"],
  "recommended_action": "specific action",
  "confidence": 0.85
}}"""

            response = await self.groq_client.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            # Parse JSON response
            content = response.get("content", "{}")
            try:
                assessment = json.loads(content)
            except json.JSONDecodeError:
                # Fallback to rule-based if AI fails
                self.logger.warning("Failed to parse AI response, using fallback")
                assessment = self.assess(complaint_data)
            
            # Add disclaimer
            assessment["disclaimer"] = "AI-assisted assessment. Requires human QA review and regulatory compliance verification."
            
            return assessment
            
        except Exception as e:
            self.logger.error(f"Error in AI risk assessment: {str(e)}")
            # Fallback to rule-based assessment
            return self.assess(complaint_data)

    def _build_complaint_summary(self, complaint: Dict[str, Any]) -> str:
        """Build a readable summary of complaint for AI"""
        lines = []
        
        fields = [
            ("Product", "product_name"),
            ("Batch Number", "batch_number"),
            ("Complaint Type", "complaint_type"),
            ("Description", "complaint_description"),
            ("Severity", "initial_severity"),
            ("Affected Quantity", "affected_quantity"),
            ("Customer", "customer_name"),
        ]
        
        for label, key in fields:
            value = complaint.get(key)
            if value:
                lines.append(f"{label}: {value}")
        
        return "\n".join(lines) if lines else "No complaint details available"
