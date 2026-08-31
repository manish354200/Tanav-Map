"""
API routes for AI Analysis
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime

router = APIRouter(prefix="/analysis", tags=["analysis"])

@router.post("/{victim_id}/analyze")
async def analyze_victim_data(victim_id: int):
    """Trigger analysis on victim's recent data"""
    
    # This would call the AI analysis services
    # For now, returning mock response
    
    return {
        "victim_id": victim_id,
        "analysis": {
            "sentiment_score": 65,
            "sentiment": "Negative",
            "emotion": "Anxiety",
            "emotion_scores": {
                "fear": 0.45,
                "anxiety": 0.68,
                "anger": 0.12,
                "sadness": 0.55,
                "stress": 0.72
            },
            "voice_stress": 0.72,
            "behavior_score": 58,
            "threat_indicators": 2,
            "threat_level": "high"
        },
        "distress_score": {
            "current": 68,
            "risk_level": "high",
            "components": {
                "sentiment": 0.30 * 65,
                "voice": 0.25 * 72,
                "behavior": 0.20 * 58,
                "threats": 0.15 * 80,
                "history": 0.10 * 50
            }
        },
        "explanation": [
            "Fear keywords increased 35%",
            "Voice stress increased 20%",
            "Missed 3 follow-ups",
            "Mentioned threats twice"
        ],
        "timestamp": datetime.now()
    }

@router.get("/{victim_id}/distress-score")
async def get_distress_score(victim_id: int):
    """Get current distress score"""
    
    return {
        "victim_id": victim_id,
        "current_score": 68,
        "risk_level": "high",
        "last_updated": datetime.now(),
        "trend": "increasing"
    }

@router.get("/{victim_id}/distress-trend")
async def get_distress_trend(victim_id: int, days: int = 30):
    """Get distress score trend over time"""
    
    # Generate mock trend data
    trend_data = []
    base_score = 50
    
    for i in range(days, 0, -1):
        trend_data.append({
            "days_ago": i,
            "score": base_score + (i * 0.5),
            "risk_level": "low" if base_score + (i * 0.5) < 30 else "medium" if base_score + (i * 0.5) < 60 else "high"
        })
    
    return {
        "victim_id": victim_id,
        "period_days": days,
        "trend": trend_data,
        "prediction": {
            "7_day_risk": 75,
            "15_day_risk": 82,
            "30_day_risk": 88
        }
    }
