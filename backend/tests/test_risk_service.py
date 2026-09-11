from app.services.risk_service import RiskService

def test_high_risk_visual_defect():
    result = RiskService().assess({"complaint_description": "Capsules show discoloration."})
    assert result["risk_level"] == "HIGH"

def test_low_risk_empty():
    result = RiskService().assess({"complaint_description": ""})
    assert result["risk_level"] == "LOW"
