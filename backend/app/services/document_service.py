from pathlib import Path
from pypdf import PdfReader
from app.services.base_service import BaseService

class DocumentService(BaseService):
    def __init__(self):
        super().__init__("document")

    def extract_pdf_text(self, file_path: str) -> str:
        reader = PdfReader(Path(file_path))
        return "\n".join(page.extract_text() or "" for page in reader.pages).strip()
