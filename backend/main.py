"""
FastAPI Application Entry Point
AI-Based Dynamic Mental Health Monitoring and Distress Prediction System
"""

from fastapi import FastAPI, Request, HTTPException, status, Depends, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import logging
import os
import random
import re
import math
import urllib.request
import urllib.error
from collections import Counter
from dotenv import load_dotenv
from datetime import datetime
from datetime import timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db import Base, engine, get_db
from app.models import Alert, DistressHistory, Interaction, Intervention, User, Victim
from app.services.distress_score_service import DistressScoreService
from app.services.sentiment_service import SentimentAnalysisService
from app.services.emotion_service import EmotionDetectionService
from app.services.voice_service import analyze_voice_stress
from app.services.predictive_service import PredictiveRiskService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-development-secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Base.metadata.create_all(bind=engine)
sentiment_service = SentimentAnalysisService(model_name=os.getenv("SENTIMENT_MODEL", "cardiffnlp/twitter-xlm-roberta-base-sentiment"))
emotion_service = EmotionDetectionService(model_name=os.getenv("EMOTION_MODEL", "SamLowe/roberta-base-go_emotions"))
predictive_service = PredictiveRiskService()

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str = "counselor"


class VictimCreateRequest(BaseModel):
    name: str
    case_type: str
    status: str = "registered"


class InteractionCreateRequest(BaseModel):
    victim_id: int
    message: str
    channel: str = "chatbot"

def create_access_token(user):
    expires = datetime.utcnow() + timedelta(minutes=30)
    payload = {"sub": user["email"], "name": user["name"], "role": user["role"], "exp": expires}
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)

def auth_response(user):
    return {"access_token": create_access_token(user), "token_type": "bearer", "name": user["name"], "email": user["email"], "role": user["role"]}

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


def serialize_victim(victim: Victim):
    return {
        "id": victim.id,
        "name": victim.name,
        "case_type": victim.case_type,
        "status": victim.status,
        "current_distress_score": victim.current_distress_score,
        "risk_level": victim.risk_level,
        "registration_date": victim.registration_date.isoformat() if victim.registration_date else None,
    }


def _risk_to_alert_level(risk_level: str) -> str:
    return {"low": "green", "medium": "yellow", "high": "orange", "critical": "red"}.get(risk_level, "yellow")


def _threat_score_from_text(text: str) -> tuple[float, int]:
    threat_terms = ["kill", "suicide", "threat", "unsafe", "attack", "violence", "die", "hurt"]
    lowered = text.lower()
    matches = sum(lowered.count(word) for word in threat_terms)
    score = min(100.0, matches * 25.0)
    return score, matches


def _behavior_score_and_missed(interactions: list[Interaction]) -> tuple[float, int]:
    if not interactions:
        return 50.0, 0
    ordered = sorted(interactions, key=lambda i: i.timestamp)
    if len(ordered) == 1:
        return 45.0, 0
    deltas = []
    for idx in range(1, len(ordered)):
        deltas.append((ordered[idx].timestamp - ordered[idx - 1].timestamp).total_seconds() / 3600.0)
    avg_gap = sum(deltas) / len(deltas)
    missed_followups = sum(1 for gap in deltas if gap > 72)
    score = min(100.0, max(20.0, 35.0 + (avg_gap * 2.5) + (missed_followups * 8.0)))
    return round(score, 2), missed_followups


def _history_score(db: Session, victim_id: int) -> float:
    latest_scores = (
        db.query(DistressHistory.score)
        .filter(DistressHistory.victim_id == victim_id)
        .order_by(DistressHistory.created_at.desc())
        .limit(10)
        .all()
    )
    if not latest_scores:
        return 50.0
    values = [item[0] for item in latest_scores]
    return round(sum(values) / len(values), 2)

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

# ============== AUTHENTICATION ==============

@app.post("/api/v1/auth/signup")
async def signup(data: SignupRequest, db: Session = Depends(get_db)):
    """Create a dashboard user and return a JWT session."""
    email = data.email.strip().lower()
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="An account with this email already exists")
    if len(data.password) < 8:
        raise HTTPException(status_code=422, detail="Password must be at least 8 characters")

    user = User(
        name=data.name.strip(),
        email=email,
        role=data.role,
        password_hash=pwd_context.hash(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return auth_response({"name": user.name, "email": user.email, "role": user.role})

@app.post("/api/v1/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Validate credentials and return a JWT session."""
    email = form_data.username.strip().lower()
    user = db.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return auth_response({"name": user.name, "email": user.email, "role": user.role})

# ============== VICTIMS ==============

@app.post("/api/v1/victims")
async def create_victim(data: VictimCreateRequest, db: Session = Depends(get_db)):
    """Register a new victim"""
    victim = Victim(
        name=data.name,
        case_type=data.case_type,
        status=data.status,
        current_distress_score=50.0,
        risk_level="medium",
    )
    db.add(victim)
    db.commit()
    db.refresh(victim)
    return serialize_victim(victim)

@app.get("/api/v1/victims")
async def list_victims(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    """List all victims"""
    items = db.query(Victim).order_by(Victim.id.asc()).all()
    start = (page - 1) * page_size
    end = start + page_size
    return {
        "total": len(items),
        "page": page,
        "page_size": page_size,
        "items": [serialize_victim(v) for v in items[start:end]]
    }

@app.get("/api/v1/victims/{victim_id}")
async def get_victim(victim_id: int, db: Session = Depends(get_db)):
    """Get victim details"""
    victim = db.query(Victim).filter(Victim.id == victim_id).first()
    if not victim:
        raise HTTPException(status_code=404, detail="Victim not found")
    return serialize_victim(victim)

# ============== INTERACTIONS ==============

@app.post("/api/v1/interactions/text")
async def log_text_interaction(payload: InteractionCreateRequest, db: Session = Depends(get_db)):
    """Log text interaction"""
    victim = db.query(Victim).filter(Victim.id == payload.victim_id).first()
    if not victim:
        raise HTTPException(status_code=404, detail="Victim not found")
    interaction = Interaction(
        victim_id=payload.victim_id,
        type="text",
        message=payload.message,
        channel=payload.channel,
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return {"interaction_id": interaction.id, "status": "received"}


@app.post("/api/v1/voice-data")
async def upload_voice_data(victim_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload voice sample and compute stress indicators."""
    victim = db.query(Victim).filter(Victim.id == victim_id).first()
    if not victim:
        raise HTTPException(status_code=404, detail="Victim not found")
    file_bytes = await file.read()
    voice_result = analyze_voice_stress(file_bytes=file_bytes, suffix=os.path.splitext(file.filename or ".wav")[1] or ".wav")
    interaction = Interaction(
        victim_id=victim_id,
        type="voice",
        message=voice_result.get("transcript") or None,
        channel="voice_upload",
        audio_file_path=file.filename or "upload",
        processed=True,
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return {
        "interaction_id": interaction.id,
        "victim_id": victim_id,
        "voice_stress_score": voice_result.get("voice_stress_score", 50.0),
        "features": voice_result.get("features", {}),
        "transcript": voice_result.get("transcript", ""),
    }

@app.get("/api/v1/interactions/{victim_id}/history")
async def get_interaction_history(victim_id: int, limit: int = 10, db: Session = Depends(get_db)):
    """Get interaction history"""
    victim_interactions = (
        db.query(Interaction)
        .filter(Interaction.victim_id == victim_id)
        .order_by(Interaction.timestamp.desc())
        .limit(limit)
        .all()
    )
    return {
        "victim_id": victim_id,
        "total_interactions": db.query(func.count(Interaction.id)).filter(Interaction.victim_id == victim_id).scalar() or 0,
        "recent_interactions": [
            {
                "id": item.id,
                "victim_id": item.victim_id,
                "type": item.type,
                "message": item.message,
                "channel": item.channel,
                "timestamp": item.timestamp.isoformat() if item.timestamp else None,
            }
            for item in reversed(victim_interactions)
        ]
    }

# ============== ANALYSIS ==============

@app.post("/api/v1/analysis/{victim_id}/analyze")
async def analyze_victim(victim_id: int, db: Session = Depends(get_db)):
    """Analyze victim data"""
    victim = db.query(Victim).filter(Victim.id == victim_id).first()
    if not victim:
        raise HTTPException(status_code=404, detail="Victim not found")
    interactions = (
        db.query(Interaction)
        .filter(Interaction.victim_id == victim_id)
        .order_by(Interaction.timestamp.desc())
        .limit(20)
        .all()
    )
    text_blob = " ".join((item.message or "") for item in interactions if item.message).strip()
    sentiment_score = sentiment_service.get_sentiment_score(text_blob)
    emotions = emotion_service.detect_emotions(text_blob)
    emotion = emotion_service.get_dominant_emotion(text_blob)
    threat_score, threat_hits = _threat_score_from_text(text_blob)
    behavior_score, missed_followups = _behavior_score_and_missed(interactions)
    avg_voice = (
        db.query(func.avg(DistressHistory.voice_score))
        .filter(DistressHistory.victim_id == victim_id)
        .scalar()
    )
    voice_score = float(avg_voice) if avg_voice is not None else 50.0
    history_score = _history_score(db, victim_id)
    distress = DistressScoreService.calculate_distress_score(
        sentiment_score=sentiment_score,
        voice_score=voice_score,
        behavior_score=behavior_score,
        threat_score=threat_score,
        history_score=history_score,
    )
    forecast = predictive_service.forecast(distress["component_scores"], distress["total_score"])
    explanations = predictive_service.explain(distress["component_scores"], distress["total_score"])
    explanations.append(f"Missed follow-ups observed: {missed_followups}.")
    if threat_hits:
        explanations.append(f"Threat indicators detected {threat_hits} times in recent interactions.")

    victim.current_distress_score = distress["total_score"]
    victim.risk_level = distress["risk_level"]
    history_entry = DistressHistory(
        victim_id=victim_id,
        score=distress["total_score"],
        risk_level=distress["risk_level"],
        sentiment_score=distress["component_scores"]["sentiment"],
        voice_score=distress["component_scores"]["voice"],
        behavior_score=distress["component_scores"]["behavior"],
        threat_score=distress["component_scores"]["threats"],
        history_score=distress["component_scores"]["history"],
    )
    db.add(history_entry)
    if distress["risk_level"] in {"high", "critical"}:
        alert = Alert(
            victim_id=victim_id,
            level=distress["risk_level"],
            title="Distress escalation detected",
            message="Automated analysis detected elevated risk requiring attention.",
            score=distress["total_score"],
        )
        db.add(alert)
    db.commit()

    return {
        "victim_id": victim_id,
        "analysis": {
            "sentiment_score": round(sentiment_score, 2),
            "sentiment": sentiment_service.analyze_text(text_blob).get("label", "neutral"),
            "emotion": emotion,
            "emotion_scores": emotions,
            "voice_stress": round(voice_score, 2),
            "behavior_score": round(behavior_score, 2),
            "threat_indicators": threat_hits,
            "threat_level": "high" if threat_score >= 70 else "medium" if threat_score >= 35 else "low",
        },
        "distress_score": {
            "current": distress["total_score"],
            "risk_level": distress["risk_level"],
            "components": distress["component_scores"],
        },
        "prediction": forecast,
        "explanation": explanations,
        "analysis_timestamp": datetime.now().isoformat(),
    }

@app.get("/api/v1/analysis/{victim_id}/distress-score")
async def get_distress_score(victim_id: int, db: Session = Depends(get_db)):
    """Get current distress score"""
    victim = db.query(Victim).filter(Victim.id == victim_id).first()
    if not victim:
        raise HTTPException(status_code=404, detail="Victim not found")
    history = (
        db.query(DistressHistory)
        .filter(DistressHistory.victim_id == victim_id)
        .order_by(DistressHistory.created_at.desc())
        .limit(2)
        .all()
    )
    trend = "stable"
    if len(history) == 2:
        trend = "increasing" if history[0].score > history[1].score else "decreasing" if history[0].score < history[1].score else "stable"
    return {
        "victim_id": victim_id,
        "current_score": victim.current_distress_score,
        "risk_level": victim.risk_level,
        "trend": trend
    }


@app.get("/api/v1/analysis/{victim_id}/distress-trend")
async def get_distress_trend(victim_id: int, days: int = 30, db: Session = Depends(get_db)):
    """Get distress trend and 7/15/30 day risk forecast."""
    victim = db.query(Victim).filter(Victim.id == victim_id).first()
    if not victim:
        raise HTTPException(status_code=404, detail="Victim not found")
    records = (
        db.query(DistressHistory)
        .filter(DistressHistory.victim_id == victim_id)
        .order_by(DistressHistory.created_at.desc())
        .limit(max(1, days))
        .all()
    )
    trend = [
        {
            "timestamp": row.created_at.isoformat() if row.created_at else None,
            "score": row.score,
            "risk_level": row.risk_level,
        }
        for row in reversed(records)
    ]
    latest_components = {
        "sentiment": records[0].sentiment_score if records else 50.0,
        "voice": records[0].voice_score if records else 50.0,
        "behavior": records[0].behavior_score if records else 50.0,
        "threats": records[0].threat_score if records else 50.0,
        "history": records[0].history_score if records else 50.0,
    }
    forecast = predictive_service.forecast(latest_components, victim.current_distress_score)
    return {"victim_id": victim_id, "period_days": days, "trend": trend, "prediction": forecast}

# ============== DASHBOARDS ==============

@app.get("/api/v1/dashboard/district")
async def district_dashboard(db: Session = Depends(get_db)):
    """District dashboard"""
    return {
        "level": "district",
        "statistics": {
            "total_victims": db.query(func.count(Victim.id)).scalar() or 0,
            "high_risk_victims": db.query(func.count(Victim.id)).filter(Victim.risk_level.in_(["high", "critical"])).scalar() or 0,
            "new_alerts_today": db.query(func.count(Alert.id)).scalar() or 0
        }
    }

@app.get("/api/v1/dashboard/state")
async def state_dashboard(db: Session = Depends(get_db)):
    """State dashboard"""
    return {
        "level": "state",
        "statistics": {
            "total_victims": db.query(func.count(Victim.id)).scalar() or 0,
            "high_risk_victims": db.query(func.count(Victim.id)).filter(Victim.risk_level.in_(["high", "critical"])).scalar() or 0
        }
    }

@app.get("/api/v1/dashboard/national")
async def national_dashboard(db: Session = Depends(get_db)):
    """National dashboard"""
    return {
        "level": "national",
        "statistics": {
            "total_victims": db.query(func.count(Victim.id)).scalar() or 0,
            "high_risk_victims": db.query(func.count(Victim.id)).filter(Victim.risk_level.in_(["high", "critical"])).scalar() or 0
        }
    }

# ============== ALERTS ==============

@app.get("/api/v1/alerts")
async def get_alerts(db: Session = Depends(get_db)):
    """Get alerts ordered from critical to low priority."""
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    alerts = sorted(
        db.query(Alert).all(),
        key=lambda alert: (
            priority_order.get(str(alert.level).lower(), 4),
            -(alert.score or 0),
            alert.created_at.isoformat() if alert.created_at else "",
        ),
    )
    return {
        "total": len(alerts),
        "alerts": [
            {
                "id": alert.id,
                "victim_id": alert.victim_id,
                "level": alert.level,
                "title": alert.title,
                "message": alert.message,
                "score": alert.score,
                "created_at": alert.created_at.isoformat() if alert.created_at else None,
                "status": "acknowledged" if alert.acknowledged else "active",
            }
            for alert in alerts
        ]
    }

@app.post("/api/v1/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: int, db: Session = Depends(get_db)):
    """Acknowledge an alert"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.acknowledged = True
    db.commit()
    return {"alert_id": alert_id, "status": "acknowledged"}

def call_openrouter(message: str, history=None, language="english"):
    """Optional OpenRouter integration for more natural conversational replies."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return None

    model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
    conversation = [
        {
            "role": "system",
            "content": f"You are a warm, friendly mental health support companion. Reply only in {language}, using simple, natural language and a culturally respectful tone. Be empathetic, conversational, and brief. Ask one gentle follow-up question when useful. Always return valid JSON with keys: reply, stress_percentage, stress_level. stress_percentage must be an integer from 0 to 100. stress_level must be one of low, moderate, high."
        }
    ]
    for item in (history or [])[-8:]:
        role = item.get("role")
        content = str(item.get("content", "")).strip()
        if role in ["user", "assistant"] and content:
            conversation.append({"role": role, "content": content[:800]})
    conversation.append({"role": "user", "content": message})

    payload = {
        "model": model,
        "messages": conversation,
        "temperature": 0.8,
        "max_tokens": 220
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "Mental Health Support Assistant"
    }

    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")[:500]
        logger.warning("OpenRouter request failed with HTTP %s: %s", error.code, error_body)
        return None
    except urllib.error.URLError as error:
        logger.warning("OpenRouter request failed: %s", error.reason)
        return None
    except (ValueError, KeyError) as error:
        logger.warning("OpenRouter response could not be parsed: %s", error)
        return None

    try:
        content = result["choices"][0]["message"]["content"]
        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```json\s*|^```\s*|\s*```$", "", cleaned, flags=re.IGNORECASE)
        try:
            parsed = json.loads(cleaned)
        except ValueError:
            json_match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group(0))
            elif cleaned:
                return {
                    "reply": cleaned,
                    "stress_percentage": 45,
                    "stress_level": "moderate"
                }
            else:
                return None
        reply = str(parsed.get("reply") or "I’m here with you.")
        stress_pct = int(parsed.get("stress_percentage", 0))
        stress_level = str(parsed.get("stress_level") or "low")
        return {
            "reply": reply,
            "stress_percentage": max(0, min(100, stress_pct)),
            "stress_level": stress_level.lower() if stress_level.lower() in ["low", "moderate", "high"] else "low"
        }
    except Exception as error:
        logger.warning("OpenRouter JSON payload was not usable: %s", error)
        return None


@app.post("/api/v1/assistant/response")
async def assistant_response(payload: dict):
    """Multilingual conversational support assistant with local retrieval and optional OpenRouter-powered responses."""
    message = str(payload.get("message", "")).strip()
    history = payload.get("history") if isinstance(payload.get("history"), list) else []
    supported_languages = {"english", "hindi", "tamil", "telugu", "bengali", "marathi", "punjabi"}
    language = str(payload.get("language", "english")).lower()
    if language not in supported_languages:
        language = "english"
    message_lower = message.lower()

    if not message:
        return {
            "reply": "Hey, I’m here with you. You can tell me anything without pressure.",
            "stress_percentage": 18,
            "stress_level": "low"
        }

    self_harm_trigger = any(phrase in message_lower for phrase in [
        "kill myself", "end my life", "suicide", "self harm", "hurt myself", "can't go on",
        "cannot go on", "dont want to live", "don't want to live"
    ])
    if self_harm_trigger:
        return {
            "reply": "I’m really sorry it feels this unbearable right now. Please stay with me for a moment: are you somewhere safe, and is there a trusted person nearby you can call or sit with right now?",
            "stress_percentage": 96,
            "stress_level": "high"
        }

    violent_trigger = any(word in message_lower for word in [
        "kill", "murder", "stab", "shoot", "attack", "hurt someone", "beat him", "kill him",
        "hurt him", "destroy him", "violence"
    ])
    if violent_trigger:
        return {
            "reply": "I hear how angry and overwhelmed you feel right now. It’s okay to feel hurt, but hurting someone is not the answer. Take a breath, move away from the situation, and tell me what happened so we can calm this down and find a safer next step.",
            "stress_percentage": 88,
            "stress_level": "high"
        }

    openrouter_result = call_openrouter(message, history, language)
    if openrouter_result:
        return openrouter_result

    def normalize(text: str):
        return re.findall(r"[a-z0-9]+|[\u0900-\u097f]+", text.lower())

    def cosine_similarity(a_tokens, b_tokens):
        if not a_tokens or not b_tokens:
            return 0.0
        a_counter = Counter(a_tokens)
        b_counter = Counter(b_tokens)
        dot = sum(a_counter[token] * b_counter[token] for token in set(a_counter) & set(b_counter))
        mag_a = math.sqrt(sum(value * value for value in a_counter.values()))
        mag_b = math.sqrt(sum(value * value for value in b_counter.values()))
        if mag_a == 0 or mag_b == 0:
            return 0.0
        return dot / (mag_a * mag_b)

    recent_user_context = " ".join(
        str(item.get("content", "")).strip()
        for item in history[-6:]
        if item.get("role") == "user" and str(item.get("content", "")).strip()
    )
    context_text = f"{recent_user_context} {message}".strip()
    lowered = context_text.lower()
    query_tokens = normalize(lowered)
    query_set = set(query_tokens)

    hindi_markers = [
        "namaste", "namaskar", "kya", "kaise", "main", "mai", "mujhe", "tum",
        "aap", "khush", "gussa", "dar", "udasi", "akela", "dost", "theek",
        "thik", "bahut", "batao", "aaj", "lagta", "samajh", "saath"
    ]
    is_hindi = any(token in hindi_markers for token in query_tokens) or any(ch in lowered for ch in ["\u0939", "\u0940", "\u092e", "\u0915", "\u093e", "\u093f", "\u094d"])

    greeting_phrases = ["hi", "hello", "hey", "good morning", "good evening", "good afternoon"]
    how_are_you_phrases = ["how are you", "how r u", "how are u", "how you doing", "how are things"]
    positive_words = ["fine", "good", "okay", "alright", "happy", "calm", "safe", "better", "relaxed", "hopeful", "theek", "thik", "khush"]
    stress_words = [
        "scared", "afraid", "unsafe", "fear", "panic", "hurt", "danger", "lonely", "sad",
        "cry", "depressed", "overwhelmed", "angry", "frustrated", "failed", "unfair", "dispute",
        "betrayed", "stress", "anxious", "hopeless", "tired", "empty", "wronged", "ego", "biased",
        "dar", "ghabra", "khauf", "udasi", "akela", "gussa", "niraasha", "fail", "teacher"
    ]

    stress_score = 10
    for word in stress_words:
        stress_score += query_tokens.count(word) * 12
    for word in positive_words:
        stress_score -= query_tokens.count(word) * 7

    if any(phrase in message_lower for phrase in greeting_phrases):
        stress_score -= 8
    if any(phrase in message_lower for phrase in how_are_you_phrases):
        stress_score -= 5

    stress_score = max(0, min(100, stress_score))

    if any(phrase in message_lower for phrase in greeting_phrases) and not any(word in lowered for word in stress_words):
        if is_hindi:
            reply = "Namaste! Main theek hoon, shukriya puchhne ke liye. Aaj kaise ho?"
        else:
            reply = "Hey! I’m good, thanks for asking. How are you doing today?"
        return {
            "reply": reply,
            "stress_percentage": int(stress_score),
            "stress_level": "low" if stress_score < 35 else "moderate" if stress_score < 65 else "high"
        }

    if any(phrase in message_lower for phrase in how_are_you_phrases):
        if is_hindi:
            reply = "Main theek hoon, shukriya puchhne ke liye. Main tumhare liye yahan hoon, aur main sunna chahta hoon ki aaj tum kaise feel kar rahe ho."
        else:
            reply = "I’m doing okay, thanks for asking. I’m here for you, and I’d love to hear how you’re feeling today."
        return {
            "reply": reply,
            "stress_percentage": int(stress_score),
            "stress_level": "low" if stress_score < 35 else "moderate" if stress_score < 65 else "high"
        }

    if any(phrase in message_lower for phrase in ["fine", "good", "okay", "alright", "theek", "thik"]) and len(normalize(message_lower)) <= 8:
        if is_hindi:
            reply = "Acha laga sun kar. Agar kuch bhi bother kar raha hai, chhota sa bhi, toh mujhe bata sakte ho."
        else:
            reply = "That’s nice to hear. I’m happy for you. If anything is bothering you, even a tiny thing, you can tell me about it anytime."
        return {
            "reply": reply,
            "stress_percentage": int(stress_score),
            "stress_level": "low" if stress_score < 35 else "moderate" if stress_score < 65 else "high"
        }

    knowledge_base = [
        {
            "topic": "teacher_bias_and_unfair_failure",
            "keywords": [
                "teacher", "failed", "fail", "grade", "marks", "ego", "bias",
                "dispute", "personal", "unfair", "score", "marksheet", "teacher", "sir", "madam"
            ],
            "content": "A student may feel harmed when a teacher fails them unfairly due to personal bias or a dispute, especially when the grading does not reflect their actual effort or performance.",
            "answer_en": "That sounds really unfair, and your feelings make sense. A personal dispute or bias should not erase your effort. Tell me a bit more about what happened, and we can look at a calm, smart next step together.",
            "answer_hi": "Lagta hai yeh bahut unfair hua hai, aur tumhari feelings sahi hain. Personal dispute ya bias tumhari mehnat ko khatam nahi kar sakta. Mujhe thoda aur batao ki kya hua, aur hum milke ek calm aur smart next step sochenge."
        },
        {
            "topic": "fear_and_threats",
            "keywords": ["scared", "afraid", "unsafe", "threat", "fear", "panic", "hurt", "danger", "dar", "ghabra", "khauf"],
            "content": "When a person feels unsafe, threatened, or afraid, they need reassurance, space to describe the risk, and a trusted plan to cope step by step.",
            "answer_en": "I’m really sorry you’re carrying that. You do not have to handle it alone. Tell me a little more about what feels unsafe or threatening, and we can take it one step at a time together.",
            "answer_hi": "Main samajh raha hoon tumhe bahut stress ho raha hoga. Tumhe ise akela nahi carry karna chahiye. Mujhe thoda aur batao ki kya unsafe ya threatening feel ho raha hai, aur hum ek-ek step mein solve karenge."
        },
        {
            "topic": "sadness_and_overwhelm",
            "keywords": ["sad", "lonely", "hopeless", "cry", "tired", "empty", "overwhelmed", "depressed", "udasi", "akela"],
            "content": "Sadness and loneliness can feel crushing when a person is overwhelmed, exhausted, or unable to share what is hurting most.",
            "answer_en": "That sounds really heavy. I’m glad you told me. It makes sense that you feel this way, and I’m here with you without judgment. What feels the hardest right now?",
            "answer_hi": "Yeh bahut heavy lag raha hai. Acha hua tumne mujhe bata diya. Tumhe aisa feel hona sahi hai, aur main tumhare saath hoon bina judge kiye. Ab sabse mushkil kya lag raha hai?"
        },
        {
            "topic": "anger_and_injustice",
            "keywords": ["angry", "frustrated", "wronged", "unfair", "disrespect", "biased", "betrayed", "gussa"],
            "content": "Anger often appears when someone feels disrespected, wronged, or treated unfairly and needs room to express the impact of that injustice.",
            "answer_en": "I hear how angry and hurt this makes you feel. It’s okay to feel that way. Let’s focus on what happened, what evidence you have, and what you want to say next in a calm and strong way.",
            "answer_hi": "Main samajh raha hoon tum kitna gussa aur hurt feel kar rahe ho. Yeh theek hai. Chalo dekhe kya hua, tumhare paas kitna evidence hai, aur tum agle step mein calm aur strong tareeke se kya kehna chahte ho."
        },
        {
            "topic": "general_support",
            "keywords": ["hello", "hi", "hey", "help", "support", "talk", "feel", "namaste", "batao"],
            "content": "A friendly supportive response should invite the user to share openly, reassure them they are safe to speak, and encourage a gentle next step.",
            "answer_en": "Hey, I’m here for you. You can share anything, even the little things, and I’ll listen without judging you. We can take it gently, one step at a time.",
            "answer_hi": "Hey, main tumhare liye hoon. Aap kuch bhi share kar sakte ho, chhote se chhota baat bhi, aur main bina judge kiye sununga. Hum isse gently, ek ek step mein handle karenge."
        },
        {
            "topic": "academic_recovery",
            "keywords": ["marks", "score", "passing", "exam", "result", "grade", "out of 70", "marks", "exam", "result"],
            "content": "When a result feels unfair, the best next step is to review evidence, organize the outcome, and plan a calm, documented response to request fairness.",
            "answer_en": "I get why that feels frustrating. If you believe your effort was better than the result, it’s okay to gather your evidence and ask for a fair review. We can work through that together.",
            "answer_hi": "Mujhe samajh aata hai tumhein yeh frustrating laga. Agar tumhe lagta hai tumhari mehnat result se better thi, toh evidence collect karna aur fair review ke liye request karna theek hai. Hum milke isko handle kar sakte hain."
        }
    ]

    scored_docs = []
    for doc in knowledge_base:
        doc_tokens = normalize(doc["topic"] + " " + " ".join(doc["keywords"]) + " " + doc["content"])
        keyword_overlap = query_set & set(doc_tokens)
        lexical_similarity = cosine_similarity(query_tokens, doc_tokens)
        score = (
            4 * len(keyword_overlap)
            + 2 * len(query_set & set(doc["keywords"]))
            + 1.5 * lexical_similarity
            + (1 if doc["topic"] in lowered else 0)
        )
        if score > 0:
            best_answer = doc["answer_hi"] if is_hindi else doc["answer_en"]
            scored_docs.append((score, best_answer, doc["topic"]))

    if scored_docs:
        _, base_answer, topic = max(scored_docs, key=lambda item: item[0])
        follow_ups_en = {
            "teacher_bias_and_unfair_failure": "What exactly did the teacher say or do after the dispute?",
            "fear_and_threats": "What is making you feel most unsafe right now?",
            "sadness_and_overwhelm": "What part of today has felt the heaviest?",
            "anger_and_injustice": "What happened just before this feeling got so strong?",
            "academic_recovery": "Do you have marks, messages, or any proof we can organize calmly?",
            "general_support": "What is on your mind right now?"
        }
        follow_ups_hi = {
            "teacher_bias_and_unfair_failure": "Dispute ke baad teacher ne exactly kya kaha ya kiya?",
            "fear_and_threats": "Abhi sabse zyada unsafe kis baat se feel ho raha hai?",
            "sadness_and_overwhelm": "Aaj ka sabse heavy part kya raha?",
            "anger_and_injustice": "Yeh feeling itni strong hone se pehle kya hua?",
            "academic_recovery": "Kya tumhare paas marks, messages, ya koi proof hai jise hum calmly organize kar sakein?",
            "general_support": "Abhi tumhare mind mein sabse zyada kya chal raha hai?"
        }
        follow_up = (follow_ups_hi if is_hindi else follow_ups_en).get(topic)
        response = f"{base_answer} {follow_up}" if follow_up and random.random() > 0.35 else base_answer
    else:
        if is_hindi:
            response = random.choice([
                "Shukriya tumne mujhe bataya. Main tumhare saath hoon. Thoda aur batao, abhi sabse zyada kya bother kar raha hai?",
                "Main sun raha hoon. Tumhe isse akela handle nahi karna hai. Kya hua, apne words mein batao.",
                "Theek hai, hum dheere dheere samjhenge. Abhi tum kis cheez ke liye support chahte ho?"
            ])
        else:
            response = random.choice([
                "I’m listening. Tell me a little more about what happened, and we’ll sort through it slowly.",
                "Thanks for opening up. What feels most important for me to understand right now?",
                "I’m here with you. We can take this gently. What has been weighing on you the most?"
            ])

    return {
        "reply": response,
        "stress_percentage": int(stress_score),
        "stress_level": "low" if stress_score < 35 else "moderate" if stress_score < 65 else "high"
    }

# ============== INTERVENTIONS ==============

@app.get("/api/v1/interventions/{victim_id}")
async def get_interventions(victim_id: int, db: Session = Depends(get_db)):
    """Get interventions for victim"""
    victim = db.query(Victim).filter(Victim.id == victim_id).first()
    if not victim:
        raise HTTPException(status_code=404, detail="Victim not found")
    interventions = db.query(Intervention).filter(Intervention.victim_id == victim_id).all()
    if not interventions:
        recommendation = Intervention(victim_id=victim_id, type="counseling", priority="high", status="pending")
        db.add(recommendation)
        db.commit()
        db.refresh(recommendation)
        interventions = [recommendation]
    return {
        "victim_id": victim_id,
        "recommendations": [
            {"type": item.type, "priority": item.priority, "status": item.status}
            for item in interventions
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
