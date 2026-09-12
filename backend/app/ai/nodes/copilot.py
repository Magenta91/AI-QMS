from app.ai.state import ComplaintGraphState
from app.clients.groq_client import GroqClient
from app.core.logging import get_logger
import json

logger = get_logger("LANGGRAPH")
groq_client = GroqClient()

async def copilot_node(state: ComplaintGraphState) -> dict:
    """Handle conversational corrections and questions about the complaint"""
    logger.info("Running copilot node")
    
    user_correction = state.get("user_correction")
    if not user_correction:
        logger.warning("No user correction data provided")
        return state
    
    user_message = user_correction.get("message", "")
    current_complaint = state.get("complaint", {})
    
    if not user_message:
        return state
    
    # Build context about current complaint
    complaint_summary = _build_complaint_context(current_complaint)
    
    prompt = f"""You are an AI assistant helping with pharmaceutical complaint management.

Current Complaint Data:
{complaint_summary}

User Message: {user_message}

Analyze the user's message and determine what they want:

1. If they're asking a QUESTION (e.g., "What's the risk level?", "Is this complete?", "What's missing?"):
   - Provide a helpful answer based on the complaint data
   - Respond with: {{"type": "answer", "response": "your answer here"}}

2. If they want to UPDATE/CORRECT a field (e.g., "Change batch number to X", "The customer name should be Y"):
   - Extract the field name and new value
   - Respond with: {{"type": "correction", "field": "field_name", "value": "new_value", "response": "I've updated the [field] to [value]"}}

3. If the request is UNCLEAR:
   - Ask for clarification
   - Respond with: {{"type": "clarification", "response": "Could you please clarify..."}}

Respond ONLY with valid JSON in one of the formats above. No markdown, no extra text.

Available fields: complaint_source, customer_name, product_name, product_strength, batch_number, affected_quantity, manufacturing_date, expiry_date, complaint_date, originating_site, affected_material, complaint_type, complaint_description, initial_severity, priority"""

    try:
        response = await groq_client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )
        
        content = response.get("content", "{}").strip()
        
        if content.startswith("```json"):
            content = content.split("```json")[1].split("```")[0].strip()
        elif content.startswith("```"):
            content = content.split("```")[1].split("```")[0].strip()
        
        result = json.loads(content)
        
        response_type = result.get("type", "answer")
        
        if response_type == "correction":
            field = result.get("field")
            value = result.get("value")
            if field and field in [
                "complaint_source", "customer_name", "product_name", "product_strength",
                "batch_number", "affected_quantity", "manufacturing_date", "expiry_date",
                "complaint_date", "originating_site", "affected_material", "complaint_type",
                "complaint_description", "initial_severity", "priority"
            ]:
                current_complaint[field] = value
                logger.info(f"Updated {field} to: {value}")
        
        return {
            **state,
            "complaint": current_complaint,
            "copilot_response": result.get("response", "I understood your message.")
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse copilot response: {str(e)}")
        return {
            **state,
            "copilot_response": "I understood your message, but I'm having trouble processing it. Could you try rephrasing?"
        }
    except Exception as e:
        logger.error(f"Copilot error: {str(e)}")
        return {
            **state,
            "copilot_response": "I encountered an error processing your message. Please try again."
        }

def _build_complaint_context(complaint: dict) -> str:
    if not complaint or not any(complaint.values()):
        return "No complaint data available yet. Please upload a document first."
    
    lines = []
    for key, value in complaint.items():
        if value:
            label = key.replace('_', ' ').title()
            lines.append(f"{label}: {value}")
    
    return "\n".join(lines) if lines else "No complaint fields populated yet."
