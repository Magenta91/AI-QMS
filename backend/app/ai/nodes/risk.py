from app.ai.state import ComplaintGraphState
from app.services.risk_service import RiskService
from app.core.logging import get_logger

logger = get_logger("LANGGRAPH")
risk_service = RiskService()

async def risk_node(state: ComplaintGraphState) -> dict:
    """Perform risk assessment on extracted complaint"""
    logger.info("Running risk assessment node")
    
    complaint = state.get("complaint", {})
    
    if not complaint or not any(complaint.values()):
        logger.warning("No complaint data for risk assessment")
        return {**state, "risk_assessment": None}
    
    try:
        assessment = await risk_service.assess_risk(complaint)
        return {**state, "risk_assessment": assessment}
    except Exception as e:
        logger.error(f"Risk assessment error: {str(e)}")
        return {**state, "risk_assessment": None, "error": str(e)}
