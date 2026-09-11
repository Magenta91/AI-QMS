from langgraph.graph import END, START, StateGraph
from app.ai.state import ComplaintGraphState
from app.ai.nodes.extraction import extraction_node
from app.ai.nodes.risk import risk_node
from app.core.logging import get_logger

logger = get_logger("LANGGRAPH")

def validation_node(state: ComplaintGraphState) -> dict:
    """Validate extracted complaint data"""
    logger.info("Running validation node")
    
    complaint = state.get("complaint", {})
    required = ["product_name", "batch_number", "complaint_description"]
    missing = [f for f in required if not complaint.get(f)]
    
    validation_errors = []
    if missing:
        validation_errors.append(f"Missing required fields: {', '.join(missing)}")
    
    return {**state, "missing_fields": missing, "validation_errors": validation_errors}

def completeness_check_node(state: ComplaintGraphState) -> dict:
    """Calculate completeness score"""
    logger.info("Running completeness check node")
    
    complaint = state.get("complaint", {})
    fields = [
        "complaint_source", "customer_name", "product_name",
        "product_strength", "batch_number", "affected_quantity",
        "manufacturing_date", "expiry_date", "complaint_date",
        "originating_site", "complaint_type", "complaint_description",
        "initial_severity", "priority"
    ]
    present = sum(1 for f in fields if complaint.get(f))
    completeness = round(present / len(fields) * 100, 1) if fields else 0.0
    
    logger.info(f"Completeness: {completeness}% ({present}/{len(fields)} fields)")
    
    return {**state, "completeness": completeness}

def create_complaint_graph():
    """Build and compile the LangGraph workflow"""
    logger.info("Creating complaint processing graph")
    
    graph = StateGraph(ComplaintGraphState)
    
    # Add nodes - using different names than state keys
    graph.add_node("extract", extraction_node)
    graph.add_node("validate", validation_node)
    graph.add_node("check_completeness", completeness_check_node)
    graph.add_node("assess_risk", risk_node)
    
    # Define edges
    graph.add_edge(START, "extract")
    graph.add_edge("extract", "validate")
    graph.add_edge("validate", "check_completeness")
    graph.add_edge("check_completeness", "assess_risk")
    graph.add_edge("assess_risk", END)
    
    return graph.compile()

# Create singleton graph instance
complaint_graph = None

def get_complaint_graph():
    """Get or create the complaint graph singleton"""
    global complaint_graph
    if complaint_graph is None:
        complaint_graph = create_complaint_graph()
    return complaint_graph
