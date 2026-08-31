"""
Pydantic schemas for Victim-related requests/responses
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class VictimStatusEnum(str, Enum):
    REGISTERED = "registered"
    UNDER_INVESTIGATION = "under_investigation"
    TRIAL_ONGOING = "trial_ongoing"
    REHABILITATION = "rehabilitation"
    COMPENSATION_RECEIVED = "compensation_received"
    CASE_CLOSED = "case_closed"

class CaseTypeEnum(str, Enum):
    RAPE = "rape"
    GANG_RAPE = "gang_rape"
    MURDER = "murder"
    GRIEVOUS_HURT = "grievous_hurt"
    ARSON = "arson"
    CASTE_VIOLENCE = "caste_violence"
    OTHER = "other"

class VictimBase(BaseModel):
    """Base schema for Victim"""
    first_name: str
    last_name: str
    date_of_birth: datetime
    gender: str
    phone_number: str
    email: Optional[EmailStr] = None
    case_type: CaseTypeEnum
    case_description: str
    district: str
    state: str

class VictimCreate(VictimBase):
    """Schema for creating a new victim"""
    pass

class VictimUpdate(BaseModel):
    """Schema for updating victim information"""
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    case_description: Optional[str] = None
    status: Optional[VictimStatusEnum] = None

class VictimResponse(VictimBase):
    """Schema for victim response"""
    id: int
    status: VictimStatusEnum
    registration_date: datetime
    last_interaction_date: Optional[datetime] = None
    current_distress_score: float = 0.0
    risk_level: str = "low"
    
    class Config:
        from_attributes = True

class VictimListResponse(BaseModel):
    """Schema for list of victims"""
    total: int
    page: int
    page_size: int
    items: List[VictimResponse]
