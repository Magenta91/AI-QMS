from fastapi import APIRouter, HTTPException
from app.services.risk_service import RiskService
from app.core.logging import get_logger

router = APIRouter(prefix="/api/risk", tags=["risk"])
logger = get_logger("API")

risk_service = RiskService()

@router.post("/assess")
async def assess_risk(complaint_data: dict):
    """Perform AI-assisted risk assessment on a complaint"""
    logger.info("Performing risk assessment")
    
    try:
        assessment = await risk_service.assess_risk(complaint_data)
        return assessment
    
    except Exception as e:
        logger.error(f"Error assessing risk: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error assessing risk: {str(e)}")
