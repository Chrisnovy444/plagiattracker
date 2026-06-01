"""
PLAGIATTRACKER - Main FastAPI application
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time
from loguru import logger

from app.config import settings
from app.database import init_db


# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    # Startup
    logger.info("🚀 Starting PLAGIATTRACKER backend...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")

    # Initialize database
    init_db()
    logger.info("✅ Database initialized")

    # Download/verify Hugging Face models
    logger.info("📦 Loading AI models...")
    try:
        from transformers import GPT2LMHeadModel, GPT2Tokenizer
        from sentence_transformers import SentenceTransformer

        # These will load from cache if already downloaded
        GPT2LMHeadModel.from_pretrained('gpt2')
        GPT2Tokenizer.from_pretrained('gpt2')
        SentenceTransformer('all-MiniLM-L6-v2')
        logger.info("✅ AI models loaded successfully")
    except Exception as e:
        logger.warning(f"⚠️  AI models not loaded: {e}")
        logger.warning("   Models will be downloaded on first use")

    logger.info(f"📧 Support email: {settings.SUPPORT_EMAIL}")
    logger.info(f"📱 Partner phone: {settings.PARTNER_PHONE}")
    logger.info("✅ Backend ready!")

    yield

    # Shutdown
    logger.info("👋 Shutting down PLAGIATTRACKER backend...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Détecteur de plagiat + contenu IA + correction automatique",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    return response


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An error occurred",
        },
    )


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "running",
        "docs": "/docs" if settings.DEBUG else None,
        "contact": {
            "support_email": settings.SUPPORT_EMAIL,
            "partner_phone": settings.PARTNER_PHONE,
        },
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for Docker/monitoring"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
    }


# Info endpoint
@app.get("/info")
async def info():
    """Get application information"""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "features": {
            "plagiarism_detection": True,
            "ai_detection": True,
            "correction": True,
            "pdf_export": True,
        },
        "supported_formats": settings.ALLOWED_EXTENSIONS,
        "max_upload_size_mb": settings.MAX_UPLOAD_SIZE_MB,
        "contact": {
            "support_email": settings.SUPPORT_EMAIL,
            "partner_phone": settings.PARTNER_PHONE,
        },
        "plans": {
            "trial": {"price": "0 FCFA", "analyses": 3, "validity": "7 jours"},
            "student": {"price": "2,500 FCFA", "analyses": 50, "validity": "30 jours"},
            "teacher": {"price": "5,000 FCFA", "analyses": 200, "validity": "30 jours"},
            "researcher": {"price": "10,000 FCFA", "analyses": 500, "validity": "30 jours"},
            "institution": {"price": "Sur devis", "analyses": "Illimité", "validity": "365 jours"},
        },
    }


# Import and include routers
from app.routers import auth, upload, report

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(upload.router, prefix="/api/v1", tags=["upload"])
app.include_router(report.router, prefix="/api/v1", tags=["report"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
