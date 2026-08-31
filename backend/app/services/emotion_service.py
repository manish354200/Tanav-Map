"""
Emotion Detection Service
"""

from typing import Dict, List
from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

class EmotionDetectionService:
    """Service for emotion detection using transformer models"""
    
    def __init__(self, model_name: str = "j-hartmann/emotion-english-distilroberta-base"):
        """Initialize emotion detection model"""
        try:
            self.model = pipeline("text-classification", model=model_name)
            logger.info(f"Loaded emotion model: {model_name}")
        except Exception as e:
            logger.error(f"Error loading emotion model: {str(e)}")
            raise
    
    def detect_emotions(self, text: str, top_k: int = None) -> List[Dict]:
        """
        Detect emotions in given text
        
        Returns:
            List of emotions with scores
        """
        try:
            # Return top emotions
            results = self.model(text[:512], top_k=top_k)
            
            emotions = {}
            for result in results:
                emotions[result["label"].lower()] = round(result["score"], 3)
            
            return emotions
        except Exception as e:
            logger.error(f"Error in emotion detection: {str(e)}")
            return {}
    
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
