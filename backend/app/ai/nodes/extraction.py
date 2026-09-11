from app.ai.state import ComplaintGraphState
from app.clients.groq_client import GroqClient
from app.core.logging import get_logger
import json

logger = get_logger("LANGGRAPH")
groq_client = GroqClient()

async def extraction_node(state: ComplaintGraphState) -> dict:
    """Extract structured complaint data from raw text using AI"""
    logger.info("Running extraction node")
    
    text = state.get("extracted_text", "")
    if not text:
        logger.warning("No text to extract from")
        return {**state, "complaint": {}, "error": "No input text provided"}
    
    prompt = f"""You are a pharmaceutical complaint data extraction AI. Extract structured information from this complaint text.

Complaint Text:
{text}

Extract the following fields if present (use null if not found):
- complaint_source: How the complaint was received (email, phone, letter, etc.)
- customer_name: Name of the customer/complainant
- product_name: Name of the pharmaceutical product
- product_strength: Strength or grade of the product
- batch_number: Batch or lot number
- affected_quantity: Quantity affected
- manufacturing_date: Manufacturing date (YYYY-MM-DD format if possible)
- expiry_date: Expiry date (YYYY-MM-DD format if possible)
- complaint_date: Date complaint was received (YYYY-MM-DD format if possible)
- originating_site: Site where product originated
- affected_material: Material affected
- complaint_type: Type/category of complaint
- complaint_description: Detailed description of the complaint
- initial_severity: Severity level (Critical, Major, Minor)
- priority: Priority (High, Medium, Low)

Respond ONLY with valid JSON in this exact format (no markdown, no extra text):
{{
  "complaint_source": "value or null",
  "customer_name": "value or null",
  "product_name": "value or null",
  "product_strength": "value or null",
  "batch_number": "value or null",
  "affected_quantity": "value or null",
  "manufacturing_date": "value or null",
  "expiry_date": "value or null",
  "complaint_date": "value or null",
  "originating_site": "value or null",
  "affected_material": "value or null",
  "complaint_type": "value or null",
  "complaint_description": "value or null",
  "initial_severity": "value or null",
  "priority": "value or null"
}}"""

    try:
        response = await groq_client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=1000
        )
        
        content = response.get("content", "{}").strip()
        
        # Remove markdown code blocks if present
        if content.startswith("```json"):
            content = content.split("```json")[1].split("```")[0].strip()
        elif content.startswith("```"):
            content = content.split("```")[1].split("```")[0].strip()
        
        complaint = json.loads(content)
        
        logger.info(f"Successfully extracted {len([v for v in complaint.values() if v])} fields")
        
        return {**state, "complaint": complaint, "error": None}
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse AI response as JSON: {str(e)}")
        return {**state, "complaint": {}, "error": f"JSON parsing error: {str(e)}"}
    except Exception as e:
        logger.error(f"Extraction error: {str(e)}")
        return {**state, "complaint": {}, "error": str(e)}
