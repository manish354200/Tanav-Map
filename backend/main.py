"""
FastAPI Application Entry Point
AI-Based Dynamic Mental Health Monitoring and Distress Prediction System
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Mental Health Monitoring & Distress Prediction API",
    description="AI-Based system for monitoring psychological distress among victims",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== MOCK DATA ==============
victims_db = {
    1: {
        "id": 1,
        "name": "Ananya Sharma",
        "case_type": "gang_rape",
        "status": "registered",
        "current_distress_score": 68,
        "risk_level": "high",
        "registration_date": "2026-08-01T09:15:00",
    },
    2: {
        "id": 2,
        "name": "Meera Iyer",
        "case_type": "sexual_harassment",
        "status": "under_investigation",
        "current_distress_score": 54,
        "risk_level": "medium",
        "registration_date": "2026-08-05T14:20:00",
    },
    3: {
        "id": 3,
        "name": "Riya Verma",
        "case_type": "domestic_violence",
        "status": "registered",
        "current_distress_score": 75,
        "risk_level": "high",
        "registration_date": "2026-08-08T11:40:00",
    },
    4: {
        "id": 4,
        "name": "Sana Khan",
        "case_type": "trauma",
        "status": "rehabilitation",
        "current_distress_score": 43,
        "risk_level": "medium",
        "registration_date": "2026-08-12T08:10:00",
    },
}

interactions_db = {
    1: {
        "id": 1,
        "victim_id": 1,
        "type": "text",
        "message": "I feel scared and unable to sleep because of the threats.",
        "channel": "chatbot",
        "timestamp": "2026-08-31T09:00:00",
    },
    2: {
        "id": 2,
        "victim_id": 1,
        "type": "text",
        "message": "I keep checking the door and feel unsafe all the time.",
        "channel": "chatbot",
        "timestamp": "2026-08-31T10:00:00",
    },
    3: {
        "id": 3,
        "victim_id": 2,
        "type": "text",
        "message": "I am anxious but trying to stay calm during the process.",
        "channel": "chatbot",
        "timestamp": "2026-08-31T11:00:00",
    },
}

alerts_db = {
    1: {
        "id": 1,
        "victim_id": 1,
        "level": "critical",
        "title": "Severe distress escalation",
        "message": "Multiple threat keywords detected and sleep disruption reported.",
        "score": 88,
        "created_at": "2026-08-31T09:35:00",
    },
    2: {
        "id": 2,
        "victim_id": 3,
        "level": "high",
        "title": "Elevated emotional risk",
        "message": "Persistent fear and emotional distress reported during recent check-ins.",
        "score": 76,
        "created_at": "2026-08-31T08:40:00",
    },
}

interventions_db = {
    1: {
        "id": 1,
        "victim_id": 1,
        "type": "counseling",
        "priority": "high",
        "status": "pending",
    }
}

# ============== ENDPOINTS ==============

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Mental Health Monitoring System",
        "timestamp": datetime.now().isoformat()
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Mental Health Monitoring & Distress Prediction System",
        "version": "1.0.0",
        "docs": "/docs",
        "api": "/api/v1"
    }

# ============== VICTIMS ==============

@app.post("/api/v1/victims")
async def create_victim(data: dict):
    """Register a new victim"""
    victim_id = len(victims_db) + 1
    victim = {
        "id": victim_id,
        **data,
        "status": "registered",
        "current_distress_score": 50.0,
        "risk_level": "medium",
        "registration_date": datetime.now().isoformat()
    }
    victims_db[victim_id] = victim
    return victim

@app.get("/api/v1/victims")
async def list_victims(page: int = 1, page_size: int = 10):
    """List all victims"""
    items = list(victims_db.values())
    start = (page - 1) * page_size
    end = start + page_size
    return {
        "total": len(items),
        "page": page,
        "page_size": page_size,
        "items": items[start:end]
    }

@app.get("/api/v1/victims/{victim_id}")
async def get_victim(victim_id: int):
    """Get victim details"""
    if victim_id not in victims_db:
        return {"error": "Victim not found"}, 404
    return victims_db[victim_id]

# ============== INTERACTIONS ==============

@app.post("/api/v1/interactions/text")
async def log_text_interaction(victim_id: int, message: str, channel: str = "chatbot"):
    """Log text interaction"""
    interaction_id = len(interactions_db) + 1
    interaction = {
        "id": interaction_id,
        "victim_id": victim_id,
        "type": "text",
        "message": message,
        "channel": channel,
        "timestamp": datetime.now().isoformat()
    }
    interactions_db[interaction_id] = interaction
    return {"interaction_id": interaction_id, "status": "received"}

@app.get("/api/v1/interactions/{victim_id}/history")
async def get_interaction_history(victim_id: int, limit: int = 10):
    """Get interaction history"""
    victim_interactions = [v for v in interactions_db.values() if v.get("victim_id") == victim_id]
    return {
        "victim_id": victim_id,
        "total_interactions": len(victim_interactions),
        "recent_interactions": victim_interactions[-limit:]
    }

# ============== ANALYSIS ==============

@app.post("/api/v1/analysis/{victim_id}/analyze")
async def analyze_victim(victim_id: int):
    """Analyze victim data"""
    return {
        "victim_id": victim_id,
        "distress_score": 68,
        "risk_level": "high",
        "analysis_timestamp": datetime.now().isoformat(),
        "components": {
            "sentiment": 65,
            "voice_stress": 72,
            "behavior": 58,
            "threats": 80,
            "history": 50
        }
    }

@app.get("/api/v1/analysis/{victim_id}/distress-score")
async def get_distress_score(victim_id: int):
    """Get current distress score"""
    victim = victims_db.get(victim_id)
    if not victim:
        return {"error": "Victim not found"}, 404
    return {
        "victim_id": victim_id,
        "current_score": victim.get("current_distress_score", 0),
        "risk_level": victim.get("risk_level", "medium"),
        "trend": "increasing"
    }

# ============== DASHBOARDS ==============

@app.get("/api/v1/dashboard/district")
async def district_dashboard():
    """District dashboard"""
    return {
        "level": "district",
        "statistics": {
            "total_victims": 156,
            "high_risk_victims": 12,
            "new_alerts_today": 3
        }
    }

@app.get("/api/v1/dashboard/state")
async def state_dashboard():
    """State dashboard"""
    return {
        "level": "state",
        "statistics": {
            "total_victims": 5234,
            "high_risk_victims": 156
        }
    }

@app.get("/api/v1/dashboard/national")
async def national_dashboard():
    """National dashboard"""
    return {
        "level": "national",
        "statistics": {
            "total_victims": 45000,
            "high_risk_victims": 3200
        }
    }

# ============== ALERTS ==============

@app.get("/api/v1/alerts")
async def get_alerts():
    """Get alerts"""
    return {
        "total": len(alerts_db),
        "alerts": list(alerts_db.values())
    }

@app.post("/api/v1/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: int):
    """Acknowledge an alert"""
    if alert_id not in alerts_db:
        return {"error": "Alert not found"}, 404
    alerts_db[alert_id]["status"] = "acknowledged"
    return {"alert_id": alert_id, "status": "acknowledged"}

@app.post("/api/v1/assistant/response")
async def assistant_response(payload: dict):
    """Create a warm, empathetic friend-like response for the victim."""
    message = str(payload.get("message", "")).strip()

    if not message:
        return {"reply": "I’m here with you. You can tell me anything without pressure."}

    lowered = message.lower()
    if any(word in lowered for word in ["scared", "afraid", "unsafe", "threat", "hurt", "panic", "fear"]):
        reply = "I’m really sorry you’re carrying that. You do not have to handle it alone. Tell me a little more, and we can take it one step at a time together."
    elif any(word in lowered for word in ["sad", "cry", "lonely", "hopeless", "tired", "empty"]):
        reply = "That sounds really heavy. It makes sense that you feel this way. I’m here to listen and stay with you while you talk through it."
    elif any(word in lowered for word in ["angry", "mad", "betrayed", "frustrated"]):
        reply = "I hear how hurt and angry this makes you feel. It’s okay to feel that. Let’s slow it down and focus on what feels safest right now."
    elif any(word in lowered for word in ["hello", "hi", "hey", "help"]):
        reply = "Hey, I’m here for you. You can share anything, even the smallest thing, and I’ll listen without judging you."
    else:
        reply = "Thank you for telling me. I’m glad you reached out. You’re not alone in this, and we can take this one moment at a time."

    return {"reply": reply}

# ============== INTERVENTIONS ==============

@app.get("/api/v1/interventions/{victim_id}")
async def get_interventions(victim_id: int):
    """Get interventions for victim"""
    return {
        "victim_id": victim_id,
        "recommendations": [
            {"type": "counseling", "priority": "high", "status": "pending"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

