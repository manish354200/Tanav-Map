"""
API routes for Dashboard endpoints
"""

from fastapi import APIRouter

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/district")
async def district_dashboard(district: str = None):
    """Get district-level dashboard statistics"""
    
    return {
        "level": "district",
        "district": district or "Sample District",
        "statistics": {
            "total_victims": 156,
            "high_risk_victims": 12,
            "new_alerts_today": 3,
            "interventions_processed": 45,
            "case_distribution": {
                "rape": 45,
                "gang_rape": 12,
                "murder": 8,
                "caste_violence": 21,
                "other": 70
            },
            "risk_distribution": {
                "low": 89,
                "medium": 55,
                "high": 12
            },
            "alert_trend": [50, 65, 52, 68, 71, 59]
        },
        "recent_alerts": [
            {
                "id": 1,
                "victim_id": 101,
                "level": "high",
                "message": "Distress score elevated",
                "timestamp": "2024-01-15 14:30:00"
            }
        ]
    }

@router.get("/state")
async def state_dashboard(state: str = None):
    """Get state-level dashboard statistics"""
    
    return {
        "level": "state",
        "state": state or "Sample State",
        "statistics": {
            "total_victims": 5234,
            "total_high_risk": 156,
            "total_alerts": 234,
            "district_comparison": [
                {"district": "District A", "victims": 1200, "high_risk": 45},
                {"district": "District B", "victims": 1100, "high_risk": 38},
                {"district": "District C", "victims": 950, "high_risk": 32},
                {"district": "District D", "victims": 984, "high_risk": 41}
            ],
            "hotspots": [
                {"district": "District A", "risk_score": 0.85},
                {"district": "District C", "risk_score": 0.72},
                {"district": "District B", "risk_score": 0.68}
            ]
        }
    }

@router.get("/national")
async def national_dashboard():
    """Get national-level dashboard statistics"""
    
    return {
        "level": "national",
        "statistics": {
            "total_victims": 45000,
            "total_high_risk": 3200,
            "total_alerts": 5600,
            "total_interventions": 8900,
            "states_overview": [
                {"state": "State A", "victims": 5200, "high_risk": 320},
                {"state": "State B", "victims": 4800, "high_risk": 280},
                {"state": "State C", "victims": 4500, "high_risk": 250}
            ],
            "trends": {
                "monthly": [3200, 3450, 3800, 4100, 4350, 4600],
                "critical_cases_trend": [250, 280, 320, 350, 380, 410]
            },
            "resource_allocation": {
                "counselors_needed": 456,
                "protection_cases": 234,
                "rehabilitation_priority": 89
            }
        }
    }
