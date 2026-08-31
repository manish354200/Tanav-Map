"""
API routes for Alert management
"""

from fastapi import APIRouter, Query
from datetime import datetime
from enum import Enum

class AlertLevel(str, Enum):
    GREEN = "green"
    YELLOW = "yellow"
    ORANGE = "orange"
    RED = "red"

router = APIRouter(prefix="/alerts", tags=["alerts"])

# Placeholder database
alerts_db = {
    1: {
        "id": 1,
        "victim_id": 101,
        "level": "red",
        "message": "Critical distress detected",
        "distress_score": 85,
        "timestamp": "2024-01-15 10:30:00",
        "acknowledged": False,
        "recipients": ["counselor_001", "district_officer_001"]
    },
    2: {
        "id": 2,
        "victim_id": 102,
        "level": "orange",
        "message": "High risk detected",
        "distress_score": 72,
        "timestamp": "2024-01-15 09:15:00",
        "acknowledged": True,
        "recipients": ["counselor_002"]
    }
}

@router.get("")
async def get_alerts(
    status: str = Query(None, enum=["acknowledged", "pending"]),
    level: str = Query(None),
    limit: int = Query(20)
):
    """Get all active alerts"""
    
    alerts = list(alerts_db.values())
    
    if status == "pending":
        alerts = [a for a in alerts if not a.get("acknowledged")]
    elif status == "acknowledged":
        alerts = [a for a in alerts if a.get("acknowledged")]
    
    if level:
        alerts = [a for a in alerts if a.get("level") == level]
    
    alerts.sort(key=lambda x: x.get("timestamp"), reverse=True)
    
    return {
        "total": len(alerts),
        "alerts": alerts[:limit]
    }

@router.get("/{alert_id}")
async def get_alert_details(alert_id: int):
    """Get detailed information about an alert"""
    
    if alert_id not in alerts_db:
        return {"error": "Alert not found"}, 404
    
    return alerts_db[alert_id]

@router.post("/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: int):
    """Acknowledge and close an alert"""
    
    if alert_id not in alerts_db:
        return {"error": "Alert not found"}, 404
    
    alerts_db[alert_id]["acknowledged"] = True
    alerts_db[alert_id]["acknowledged_timestamp"] = datetime.now()
    
    return {
        "message": "Alert acknowledged",
        "alert_id": alert_id,
        "timestamp": datetime.now()
    }

@router.get("/{victim_id}/victim-alerts")
async def get_victim_alerts(victim_id: int):
    """Get all alerts for a specific victim"""
    
    victim_alerts = [
        a for a in alerts_db.values() 
        if a.get("victim_id") == victim_id
    ]
    
    return {
        "victim_id": victim_id,
        "total_alerts": len(victim_alerts),
        "alerts": victim_alerts
    }
