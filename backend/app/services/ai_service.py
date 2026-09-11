from app.core.config import settings
from app.services.base_service import BaseService

class AIService(BaseService):
    def __init__(self):
        super().__init__("ai")
        self.model = settings.groq_model

    def model_name(self) -> str:
        return self.model
