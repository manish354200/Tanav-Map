"""
Health check endpoints
"""

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

@router.get("")
async def health_check():
    """Check system health"""
    return {
        "status": "healthy",
        "service": "Mental Health Monitoring System",
        "version": "1.0.0"
    }

@router.get("/ready")
async def readiness_check():
    """Check if system is ready to serve requests"""
    return {
        "ready": True,
        "service": "Mental Health Monitoring System"
    }
