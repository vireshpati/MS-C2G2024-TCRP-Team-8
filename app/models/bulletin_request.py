from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from user import User

class Comment(BaseModel):
    comment_uid: str  
    post_uid: str
    author_uid: str
    content: str
    created: datetime    

class Request(BaseModel):
    post_uid: str    
    author_uid: str
    created: datetime 
    title: str
    content: str
    tag: Optional[str] = 'others'       # intended to be 'babysitting', 'tutoring', 'pickupchild', 'mealshare', 'needride', 'others'...
    location_of_help: Optional[str] = None
    date_help_needed: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    confirm_by: Optional[datetime] = None
    resolved: bool = False
    number_of_comments: int = 0
    deleted: bool = False
