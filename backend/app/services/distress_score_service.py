"""
Distress Score Calculation Service
"""

from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class DistressScoreService:
    """Service for calculating weighted distress scores"""
    
    # Weights for each component
    WEIGHTS = {
        "sentiment": 0.30,
        "voice": 0.25,
        "behavior": 0.20,
        "threats": 0.15,
        "history": 0.10
    }
    
    # Risk thresholds
    RISK_THRESHOLDS = {
        "low": (0, 30),
        "medium": (31, 60),
        "high": (61, 80),
        "critical": (81, 100)
    }
    
    @staticmethod
    def calculate_distress_score(
        sentiment_score: float,
        voice_score: float,
        behavior_score: float,
        threat_score: float,
        history_score: float
    ) -> Dict:
        """
        Calculate weighted distress score
        
        Args:
            sentiment_score: 0-100 sentiment analysis score
            voice_score: 0-100 voice stress analysis score
            behavior_score: 0-100 behavioral analytics score
            threat_score: 0-100 threat detection score
            history_score: 0-100 historical trend score
        
        Returns:
            Dict with total score and risk level
        """
        # Normalize scores to 0-100 range
        scores = {
            "sentiment": min(max(sentiment_score, 0), 100),
            "voice": min(max(voice_score, 0), 100),
            "behavior": min(max(behavior_score, 0), 100),
            "threats": min(max(threat_score, 0), 100),
            "history": min(max(history_score, 0), 100)
        }
        
        # Calculate weighted score
        total_score = sum(
            scores[key] * DistressScoreService.WEIGHTS[key]
            for key in scores.keys()
        )
        
        # Determine risk level
        risk_level = DistressScoreService._get_risk_level(total_score)
        
        return {
            "total_score": round(total_score, 2),
            "risk_level": risk_level,
            "component_scores": scores,
            "weights": DistressScoreService.WEIGHTS
        }
    
    @staticmethod
    def _get_risk_level(score: float) -> str:
        """Determine risk level based on score"""
        for level, (min_val, max_val) in DistressScoreService.RISK_THRESHOLDS.items():
            if min_val <= score <= max_val:
                return level
        return "critical"
    
    @staticmethod
    def should_trigger_alert(
        current_score: float,
        previous_score: float = None
    ) -> tuple[bool, str]:
        """
        Determine if alert should be triggered
        
        Returns:
            Tuple of (should_alert, alert_level)
        """
        current_level = DistressScoreService._get_risk_level(current_score)
        
        # Alert levels: green, yellow, orange, red
        alert_mapping = {
            "low": ("green", False),
            "medium": ("yellow", False),
            "high": ("orange", True),
            "critical": ("red", True)
        }
        
        alert_level, should_alert = alert_mapping[current_level]
        
        # Also alert if score increased significantly
        if previous_score is not None and (current_score - previous_score) > 20:
            should_alert = True
        
        return should_alert, alert_level
