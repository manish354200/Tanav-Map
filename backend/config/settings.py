"""
Configuration Settings for the Application
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    app_name: str = "Mental Health Monitoring System"
    app_version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/mental_health"
    mongodb_url: str = "mongodb://localhost:27017/mental_health_logs"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: str = "http://localhost:3000,http://localhost:5173"
    allowed_hosts: str = "localhost,127.0.0.1"
    
    # AI Models
    sentiment_model: str = "twitter-roberta-base-sentiment"
    emotion_model: str = "j-hartmann/emotion-english-distilroberta-base"
    multilingual_model: str = "muril-base-cased"
    voice_model: str = "openai/whisper-base"
    
    # Feature Weights for Distress Score
    sentiment_weight: float = 0.30
    voice_weight: float = 0.25
    behavior_weight: float = 0.20
    threat_weight: float = 0.15
    history_weight: float = 0.10
    
    # Alert Thresholds
    low_risk_threshold: int = 30
    medium_risk_threshold: int = 60
    high_risk_threshold: int = 80
    
    # Prediction
    prediction_days: list = [7, 15, 30]
    prediction_model: str = "xgboost"  # xgboost, lightgbm, lstm
    
    # Logging
    log_level: str = "INFO"
    
    # Redis (for caching)
    redis_url: str = "redis://localhost:6379/0"
    cache_ttl: int = 3600  # 1 hour
    
    # Celery (for async tasks)
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
