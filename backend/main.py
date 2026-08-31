"""
FastAPI Application Entry Point
AI-Based Dynamic Mental Health Monitoring and Distress Prediction System
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import routers
from app.routes import (
    victims_router,
    interactions_router,
    analysis_router,
    dashboard_router,
    alerts_router,
    interventions_router,
    health_router
)

# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    logger.info("Starting Mental Health Monitoring System...")
    yield
    # Shutdown
    logger.info("Shutting down Mental Health Monitoring System...")

# Create FastAPI application
app = FastAPI(
    title="Mental Health Monitoring & Distress Prediction API",
    description="AI-Based system for monitoring psychological distress among victims",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

# Include routers
app.include_router(health_router.router, tags=["Health"])
app.include_router(victims_router.router, prefix="/api/v1", tags=["Victims"])
app.include_router(interactions_router.router, prefix="/api/v1", tags=["Interactions"])
app.include_router(analysis_router.router, prefix="/api/v1", tags=["Analysis"])
app.include_router(dashboard_router.router, prefix="/api/v1", tags=["Dashboards"])
app.include_router(alerts_router.router, prefix="/api/v1", tags=["Alerts"])
app.include_router(interventions_router.router, prefix="/api/v1", tags=["Interventions"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Mental Health Monitoring & Distress Prediction System",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Mental Health Monitoring System"
    }

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "True").lower() == "true"
    )
