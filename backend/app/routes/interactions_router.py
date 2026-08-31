"""
API routes for Victim Interactions (data collection)
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/interactions", tags=["interactions"])

# Placeholder database
interactions_db = {}
interaction_id_counter = 1

@router.post("/text")
async def log_text_interaction(
    victim_id: int,
    message: str,
    channel: str = "chatbot"  # chatbot, mobile, helpline, etc.
):
    """Log text-based interaction from victim"""
    global interaction_id_counter
    
    interaction = {
        "id": interaction_id_counter,
        "victim_id": victim_id,
        "type": "text",
        "message": message,
        "channel": channel,
        "timestamp": datetime.now(),
        "processed": False,
    }
    
    interactions_db[interaction_id_counter] = interaction
    interaction_id_counter += 1
    
    return {
        "interaction_id": interaction["id"],
        "status": "received",
        "message": "Text interaction logged successfully"
    }

@router.post("/voice")
async def log_voice_interaction(
    victim_id: int,
    file: UploadFile = File(...),
    channel: str = "ivrs"
):
    """Log voice-based interaction from victim"""
    global interaction_id_counter
    
    # In production, save the file to storage and process asynchronously
    interaction = {
        "id": interaction_id_counter,
        "victim_id": victim_id,
        "type": "voice",
        "filename": file.filename,
        "channel": channel,
        "timestamp": datetime.now(),
        "processed": False,
    }
    
    interactions_db[interaction_id_counter] = interaction
    interaction_id_counter += 1
    
    return {
        "interaction_id": interaction["id"],
        "status": "received",
        "message": "Voice interaction logged successfully"
    }

@router.get("/{victim_id}/history")
async def get_interaction_history(
    victim_id: int,
    limit: int = 10
):
    """Get interaction history for a victim"""
    victim_interactions = [
        v for v in interactions_db.values() 
        if v.get("victim_id") == victim_id
    ]
    
    # Sort by timestamp (most recent first)
    victim_interactions.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return {
        "victim_id": victim_id,
        "total_interactions": len(victim_interactions),
        "recent_interactions": victim_interactions[:limit]
    }
