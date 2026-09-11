from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from app.schemas.complaint import ComplaintProcessRequest, ComplaintResponse, ComplaintCorrectRequest
from app.services.complaint_service import ComplaintService
from app.services.document_service import DocumentService
from app.core.logging import get_logger
import tempfile
from pathlib import Path

router = APIRouter(prefix="/api/complaints", tags=["complaints"])
logger = get_logger("API")

complaint_service = ComplaintService()
document_service = DocumentService()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and extract text from a complaint document (PDF)"""
    logger.info(f"Received file upload: {file.filename}")
    
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        # Extract text from PDF
        extracted_text = document_service.extract_pdf_text(temp_path)
        
        # Clean up temp file
        Path(temp_path).unlink()
        
        logger.info(f"Successfully extracted {len(extracted_text)} characters from PDF")
        
        return {
            "success": True,
            "filename": file.filename,
            "extracted_text": extracted_text,
            "char_count": len(extracted_text)
        }
    
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@router.post("/process")
async def process_complaint(request: ComplaintProcessRequest):
    """Process complaint text through LangGraph AI workflow"""
    logger.info("Processing complaint through AI workflow")
    
    try:
        result = await complaint_service.process_complaint(
            text=request.text,
            source_type=request.source_type
        )
        return result
    
    except Exception as e:
        logger.error(f"Error processing complaint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing complaint: {str(e)}")

@router.post("/correct")
async def correct_complaint(request: ComplaintCorrectRequest):
    """Correct a complaint field via conversational AI"""
    logger.info(f"Correcting complaint field: {request.field}")
    
    try:
        result = await complaint_service.correct_complaint(
            complaint_data=request.complaint_data,
            user_message=request.user_message,
            field=request.field
        )
        return result
    
    except Exception as e:
        logger.error(f"Error correcting complaint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error correcting complaint: {str(e)}")

@router.post("", response_model=ComplaintResponse)
async def save_complaint(complaint: dict):
    """Save complaint to database"""
    logger.info("Saving complaint to database")
    
    try:
        saved = await complaint_service.save_complaint(complaint)
        return saved
    
    except Exception as e:
        logger.error(f"Error saving complaint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error saving complaint: {str(e)}")

@router.get("/{complaint_id}", response_model=ComplaintResponse)
async def get_complaint(complaint_id: int):
    """Retrieve a complaint by ID"""
    logger.info(f"Retrieving complaint {complaint_id}")
    
    try:
        complaint = await complaint_service.get_complaint(complaint_id)
        if not complaint:
            raise HTTPException(status_code=404, detail="Complaint not found")
        return complaint
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving complaint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving complaint: {str(e)}")
