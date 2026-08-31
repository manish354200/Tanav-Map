"""
API routes for Intervention recommendations
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from enum import Enum

class InterventionType(str, Enum):
    COUNSELING = "counseling"
    WITNESS_PROTECTION = "witness_protection"
    FINANCIAL_ASSISTANCE = "financial_assistance"
    RELOCATION_SUPPORT = "relocation_support"
    PSYCHIATRIC_REFERRAL = "psychiatric_referral"
    LEGAL_AID = "legal_aid"
    REHABILITATION = "rehabilitation"

router = APIRouter(prefix="/interventions", tags=["interventions"])

# Placeholder database
interventions_db = {}

@router.get("/{victim_id}")
async def get_interventions(victim_id: int):
    """Get recommended interventions for a victim"""
    
    # These would be generated based on the distress score and risk factors
    recommended_interventions = []
    
    # Mock logic based on distress score
    distress_score = 72  # This would come from analysis
    
    if distress_score > 80:
        recommended_interventions.extend([
            InterventionType.PSYCHIATRIC_REFERRAL,
            InterventionType.WITNESS_PROTECTION
        ])
    elif distress_score > 60:
        recommended_interventions.extend([
            InterventionType.COUNSELING,
            InterventionType.FINANCIAL_ASSISTANCE
        ])
    else:
        recommended_interventions.append(InterventionType.COUNSELING)
    
    return {
        "victim_id": victim_id,
        "distress_score": distress_score,
        "recommendations": [
            {
                "type": intervention,
                "priority": "high" if distress_score > 80 else "medium",
                "description": f"Recommended {intervention.value} intervention",
                "recommended_timestamp": datetime.now(),
                "status": "pending"
            }
            for intervention in recommended_interventions
        ]
    }

@router.post("/{victim_id}/recommend")
async def create_intervention(
    victim_id: int,
    intervention_type: InterventionType,
    notes: str = None
):
    """Create a new intervention recommendation"""
    
    intervention = {
        "id": len(interventions_db) + 1,
        "victim_id": victim_id,
        "type": intervention_type,
        "notes": notes,
        "status": "pending",
        "created_timestamp": datetime.now(),
        "approved_by": None,
        "approved_timestamp": None
    }
    
    interventions_db[intervention["id"]] = intervention
    
    return intervention

@router.post("/{intervention_id}/approve")
async def approve_intervention(
    intervention_id: int,
    approved_by: str
):
    """Approve an intervention (human-in-the-loop)"""
    
    if intervention_id not in interventions_db:
        raise HTTPException(status_code=404, detail="Intervention not found")
    
    intervention = interventions_db[intervention_id]
    intervention["status"] = "approved"
    intervention["approved_by"] = approved_by
    intervention["approved_timestamp"] = datetime.now()
    
    return {
        "message": "Intervention approved",
        "intervention": intervention
    }

@router.post("/{intervention_id}/execute")
async def execute_intervention(intervention_id: int):
    """Execute/implement an approved intervention"""
    
    if intervention_id not in interventions_db:
        raise HTTPException(status_code=404, detail="Intervention not found")
    
    intervention = interventions_db[intervention_id]
    
    if intervention["status"] != "approved":
        raise HTTPException(status_code=400, detail="Intervention must be approved first")
    
    intervention["status"] = "executed"
    intervention["executed_timestamp"] = datetime.now()
    
    return {
        "message": "Intervention executed",
        "intervention": intervention
    }

@router.get("/{victim_id}/history")
async def get_intervention_history(victim_id: int):
    """Get intervention history for a victim"""
    
    victim_interventions = [
        v for v in interventions_db.values() 
        if v.get("victim_id") == victim_id
    ]
    
    return {
        "victim_id": victim_id,
        "total_interventions": len(victim_interventions),
        "interventions": victim_interventions
    }
