from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    user_id: str
    name: str
    email: EmailStr
    phone: Optional[str]
    birthday: datetime
    gender: Optional[str]
    bio: Optional[str] = ""
    interests: List[str] = []
    community_role: str = 'member'
    profile_picture: Optional[str] = None
    location: Optional[str] = None
    approved: bool = False
    active: bool = False
    created_at: datetime = datetime.utcnow()
    points: int = 0
    fcmToken: Optional[str]
