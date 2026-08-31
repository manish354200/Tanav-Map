"""
API routes for Victim management
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.schemas.victim import VictimCreate, VictimUpdate, VictimResponse, VictimListResponse

router = APIRouter(prefix="/victims", tags=["victims"])

# Placeholder database
victims_db = {}
victim_id_counter = 1

@router.post("", response_model=VictimResponse)
async def create_victim(victim: VictimCreate):
    """Register a new victim"""
    global victim_id_counter
    victim_dict = victim.model_dump()
    victim_dict["id"] = victim_id_counter
    victim_dict["status"] = "registered"
    victim_dict["current_distress_score"] = 50.0
    victim_dict["risk_level"] = "medium"
    victim_dict["last_interaction_date"] = None
    
    from datetime import datetime
    victim_dict["registration_date"] = datetime.now()
    
    victims_db[victim_id_counter] = victim_dict
    victim_id_counter += 1
    
    return victim_dict

@router.get("", response_model=VictimListResponse)
async def list_victims(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: str = Query(None),
    district: str = Query(None),
):
    """List all victims with pagination and filters"""
    items = list(victims_db.values())
    
    if status:
        items = [v for v in items if v.get("status") == status]
    if district:
        items = [v for v in items if v.get("district") == district]
    
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items[start:end]
    }

@router.get("/{victim_id}", response_model=VictimResponse)
async def get_victim(victim_id: int):
    """Get victim details"""
    if victim_id not in victims_db:
        raise HTTPException(status_code=404, detail="Victim not found")
    return victims_db[victim_id]

@router.put("/{victim_id}", response_model=VictimResponse)
async def update_victim(victim_id: int, victim: VictimUpdate):
    """Update victim information"""
    if victim_id not in victims_db:
        raise HTTPException(status_code=404, detail="Victim not found")
    
    existing = victims_db[victim_id]
    update_data = victim.model_dump(exclude_unset=True)
    existing.update(update_data)
    
    return existing

@router.delete("/{victim_id}")
async def delete_victim(victim_id: int):
    """Delete victim record"""
    if victim_id not in victims_db:
        raise HTTPException(status_code=404, detail="Victim not found")
    
    del victims_db[victim_id]
    return {"message": "Victim deleted successfully"}
