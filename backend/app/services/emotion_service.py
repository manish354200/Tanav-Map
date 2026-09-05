"""Emotion detection service with lazy loading and offline fallback."""

from functools import lru_cache
import logging
from typing import Dict

logger = logging.getLogger(__name__)

try:
    from transformers import pipeline
except Exception:  # pragma: no cover
    pipeline = None

class EmotionDetectionService:
    """Service for emotion detection using transformer models"""
    
    def __init__(self, model_name: str = "SamLowe/roberta-base-go_emotions"):
        """Initialize emotion detection model"""
        self.model_name = model_name
        self.model = None

    @staticmethod
    @lru_cache(maxsize=4)
    def _load_pipeline(model_name: str):
        if pipeline is None:
            raise RuntimeError("transformers pipeline unavailable")
        return pipeline("text-classification", model=model_name, top_k=None)

    def _ensure_model(self):
        if self.model is None:
            self.model = self._load_pipeline(self.model_name)
            logger.info("Loaded emotion model: %s", self.model_name)
    
    def detect_emotions(self, text: str, top_k: int | None = None) -> Dict:
        """
        Detect emotions in given text
        
        Returns:
            List of emotions with scores
        """
        try:
            self._ensure_model()
            # Return top emotions
            results = self.model(text[:512], top_k=top_k)
            if results and isinstance(results[0], list):
                results = results[0]
            emotions = {}
            for result in results:
                emotions[result["label"].lower()] = round(result["score"], 3)
            
            return emotions
        except Exception as e:
            logger.error(f"Error in emotion detection: {str(e)}")
            lowered = text.lower()
            return {
                "fear": 0.75 if any(word in lowered for word in ["fear", "scared", "unsafe"]) else 0.05,
                "anxiety": 0.7 if any(word in lowered for word in ["anxious", "panic", "worry"]) else 0.1,
                "anger": 0.7 if any(word in lowered for word in ["angry", "rage", "hate"]) else 0.05,
                "sadness": 0.7 if any(word in lowered for word in ["sad", "hopeless", "cry"]) else 0.1,
                "stress": 0.75 if any(word in lowered for word in ["stress", "overwhelmed", "tired"]) else 0.1,
            }
    
    def get_dominant_emotion(self, text: str) -> str:
        """Get the dominant emotion for the text"""
        emotions = self.detect_emotions(text)
        if emotions:
            return max(emotions, key=emotions.get)
        return "neutral"
    
    def is_crisis_emotion(self, text: str) -> bool:
        """Check if text contains crisis-level emotions"""
        emotions = self.detect_emotions(text)
        
        crisis_emotions = ["fear", "sadness", "anger", "disgust"]
        for emotion in crisis_emotions:
            if emotions.get(emotion, 0) > 0.7:
                return True
        
        return False
