from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import complaint_routes, risk_routes
from app.core.database import init_db
from app.core.logging import get_logger

logger = get_logger("APP")

app = FastAPI(title=settings.app_name, version="0.1.0")

# Initialize database tables on startup
@app.on_event("startup")
async def startup_event():
    logger.info("Initializing database tables...")
    try:
        init_db()
        logger.info("Database tables initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(complaint_routes.router)
app.include_router(risk_routes.router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "aivoa-backend"}
