from app.services.base_service import BaseService
from app.services.ai_service import AIService
from app.ai.graph import get_complaint_graph
from typing import Dict, Any, Optional

class ComplaintService(BaseService):
    def __init__(self):
        super().__init__("complaint")
        self.ai_service = AIService()
        self._graph = None

    @property
    def graph(self):
        if self._graph is None:
            self._graph = get_complaint_graph()
        return self._graph

    def missing_required_fields(self, complaint: dict) -> list[str]:
        required = ["product_name", "batch_number", "complaint_description"]
        return [f for f in required if not complaint.get(f)]

    async def process_complaint(self, text: str, source_type: str = "text") -> Dict[str, Any]:
        """Process complaint text through LangGraph AI workflow"""
        self.logger.info(f"Processing complaint from {source_type}")
        
        try:
            # Run the LangGraph workflow
            initial_state = {
                "raw_input": text,
                "source_type": source_type,
                "extracted_text": text,
                "complaint": {},
                "missing_fields": [],
                "validation_errors": [],
                "completeness": 0.0,
                "risk_assessment": None,
                "user_correction": None,
                "error": None
            }
            
            result = await self.graph.ainvoke(initial_state)
            
            return {
                "success": True,
                "complaint": result.get("complaint", {}),
                "missing_fields": result.get("missing_fields", []),
                "validation_errors": result.get("validation_errors", []),
                "completeness": result.get("completeness", 0.0),
                "risk_assessment": result.get("risk_assessment"),
                "error": result.get("error")
            }
            
        except Exception as e:
            self.logger.error(f"Error processing complaint: {str(e)}")
            raise

    async def correct_complaint(
        self, 
        complaint_data: Dict[str, Any], 
        user_message: str,
        field: Optional[str] = None
    ) -> Dict[str, Any]:
        """Correct a complaint field via conversational AI"""
        self.logger.info(f"Correcting complaint: {user_message[:50]}...")
        
        try:
            from app.ai.nodes.copilot import copilot_node
            
            # Run through copilot node
            correction_state = {
                "raw_input": user_message,
                "source_type": "correction",
                "extracted_text": user_message,
                "complaint": complaint_data,
                "missing_fields": [],
                "validation_errors": [],
                "completeness": 0.0,
                "risk_assessment": None,
                "user_correction": {"message": user_message, "field": field},
                "copilot_response": "",
                "error": None
            }
            
            result = await copilot_node(correction_state)
            
            return {
                "success": True,
                "complaint": result.get("complaint", complaint_data),
                "response": result.get("copilot_response", "I've processed your message."),
                "missing_fields": self.missing_required_fields(result.get("complaint", {})),
                "completeness": self._calculate_completeness(result.get("complaint", {}))
            }
            
        except Exception as e:
            self.logger.error(f"Error in copilot correction: {str(e)}")
            raise
    
    def _calculate_completeness(self, complaint: Dict[str, Any]) -> float:
        """Calculate completeness percentage"""
        fields = [
            "complaint_source", "customer_name", "product_name",
            "product_strength", "batch_number", "affected_quantity",
            "manufacturing_date", "expiry_date", "complaint_date",
            "originating_site", "complaint_type", "complaint_description",
            "initial_severity", "priority"
        ]
        present = sum(1 for f in fields if complaint.get(f))
        return round(present / len(fields) * 100, 1) if fields else 0.0

    async def save_complaint(self, complaint: Dict[str, Any]) -> Dict[str, Any]:
        """Save complaint to database"""
        self.logger.info("Saving complaint to database")
        
        try:
            from app.core.database import SessionLocal
            from app.repositories.complaint_repository import ComplaintRepository
            
            # Calculate completeness before saving
            completeness = self._calculate_completeness(complaint)
            
            # Filter to only include fields that exist in the database model
            valid_fields = [
                "complaint_source", "customer_name", "product_name", "product_strength",
                "batch_number", "affected_quantity", "manufacturing_date", "expiry_date",
                "complaint_date", "originating_site", "affected_material", "complaint_type",
                "complaint_description", "initial_severity", "priority", "completeness", "risk_assessment"
            ]
            
            # Prepare data for database - only include valid fields
            db_data = {
                key: value for key, value in complaint.items() 
                if key in valid_fields and value is not None
            }
            db_data["completeness"] = completeness
            
            # Create database session
            db = SessionLocal()
            try:
                repo = ComplaintRepository(db)
                db_complaint = repo.create(db_data)
                
                self.logger.info(f"Complaint saved with ID: {db_complaint.id}")
                
                return {
                    "id": db_complaint.id,
                    "complaint": db_complaint.to_dict(),
                    "created_at": db_complaint.created_at.isoformat() if db_complaint.created_at else None
                }
            finally:
                db.close()
                
        except Exception as e:
            self.logger.error(f"Error saving complaint: {str(e)}")
            raise

    async def get_complaint(self, complaint_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve complaint from database"""
        self.logger.info(f"Retrieving complaint {complaint_id}")
        
        try:
            from app.core.database import SessionLocal
            from app.repositories.complaint_repository import ComplaintRepository
            
            db = SessionLocal()
            try:
                repo = ComplaintRepository(db)
                db_complaint = repo.get_by_id(complaint_id)
                
                if db_complaint:
                    return {
                        "id": db_complaint.id,
                        "complaint": db_complaint.to_dict()
                    }
                return None
            finally:
                db.close()
                
        except Exception as e:
            self.logger.error(f"Error retrieving complaint: {str(e)}")
            raise
