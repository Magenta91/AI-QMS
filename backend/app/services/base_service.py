from app.core.logging import get_logger

class BaseService:
    def __init__(self, service_name: str):
        self.logger = get_logger(service_name)
