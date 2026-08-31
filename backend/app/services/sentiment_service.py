"""
Sentiment Analysis Service
"""

from typing import Dict
from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

class SentimentAnalysisService:
    """Service for sentiment analysis using transformer models"""
    
    def __init__(self, model_name: str = "twitter-roberta-base-sentiment"):
        """Initialize sentiment analysis model"""
        try:
            self.model = pipeline("sentiment-analysis", model=model_name)
            logger.info(f"Loaded sentiment model: {model_name}")
        except Exception as e:
            logger.error(f"Error loading sentiment model: {str(e)}")
            raise
    
    def analyze_text(self, text: str) -> Dict:
        """
        Analyze sentiment of given text
        
        Returns:
            Dict with sentiment label and score
        """
        try:
            result = self.model(text[:512])[0]  # Limit to 512 chars
            return {
                "label": result["label"].lower(),
                "score": round(result["score"], 3),
                "text": text[:100]
            }
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            return {"label": "unknown", "score": 0.0}
    
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
