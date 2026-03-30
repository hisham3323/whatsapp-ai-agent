import logging
from fastapi import FastAPI
from app.core.config import settings
from app.api import webhook_router

# Configure basic logging for our application
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json" if settings.DEBUG else None,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Include our webhook router
app.include_router(webhook_router, prefix="/api/v1", tags=["WhatsApp"])

@app.get("/health")
async def health_check():
    """
    Basic health check endpoint to verify the API is running.
    """
    return {
        "status": "ok",
        "project": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT
    }