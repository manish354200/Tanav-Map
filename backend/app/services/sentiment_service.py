"""Sentiment analysis service with multilingual fallback and lazy model caching."""

from functools import lru_cache
import logging
from typing import Dict

logger = logging.getLogger(__name__)

try:
    from transformers import pipeline
except Exception:  # pragma: no cover - transformer import may be unavailable in constrained envs
    pipeline = None

class SentimentAnalysisService:
    """Service for sentiment analysis using transformer models"""
    
    def __init__(self, model_name: str = "cardiffnlp/twitter-xlm-roberta-base-sentiment"):
        """Initialize sentiment analysis model"""
        self.model_name = model_name
        self.model = None
    
    @staticmethod
    @lru_cache(maxsize=4)
    def _load_pipeline(model_name: str):
        if pipeline is None:
            raise RuntimeError("transformers pipeline unavailable")
        return pipeline("sentiment-analysis", model=model_name)
    
    def _ensure_model(self):
        if self.model is None:
            self.model = self._load_pipeline(self.model_name)
            logger.info("Loaded sentiment model: %s", self.model_name)
    
    def analyze_text(self, text: str) -> Dict:
        """
        Analyze sentiment of given text
        
        Returns:
            Dict with sentiment label and score
        """
        if not text:
            return {"label": "neutral", "score": 0.0, "text": ""}
        try:
            self._ensure_model()
            result = self.model(text[:512])[0]  # Limit to 512 chars
            label = str(result["label"]).lower()
            if "neg" in label:
                label = "negative"
            elif "pos" in label:
                label = "positive"
            else:
                label = "neutral"
            return {
                "label": label,
                "score": round(result["score"], 3),
                "text": text[:100]
            }
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            lowered = text.lower()
            negatives = ["scared", "afraid", "unsafe", "anxious", "hopeless", "sad", "fear"]
            positives = ["safe", "better", "calm", "good", "hopeful"]
            neg_hits = sum(word in lowered for word in negatives)
            pos_hits = sum(word in lowered for word in positives)
            if neg_hits > pos_hits:
                return {"label": "negative", "score": 0.6, "text": text[:100]}
            if pos_hits > neg_hits:
                return {"label": "positive", "score": 0.6, "text": text[:100]}
            return {"label": "neutral", "score": 0.5, "text": text[:100]}
    
    def get_sentiment_score(self, text: str) -> float:
        """
        Get numeric sentiment score (0-100)
        Negative: 0-40, Neutral: 40-60, Positive: 60-100
        """
        result = self.analyze_text(text)
        
        if result["label"] == "positive":
            return 60 + (result["score"] * 40)
        elif result["label"] == "negative":
            return 40 - (result["score"] * 40)
        else:
            return 50
