from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# placeholders vvv
class UserBase(BaseModel):
    title: str
    description: str | None = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    class Config:
        orm_mode = True
# placeholders ^^^

class CommentBase(BaseModel):
    post_uid: int
    author_uid: int
    content: str

class RequestBase(BaseModel):
    title: str
    content: str
    tag: Optional[str] = 'others'
    location_of_help: Optional[str] = None
    date_help_needed: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    confirm_by: Optional[datetime] = None

class RequestCreate(RequestBase):
    pass


class Request(RequestBase):
    post_uid: int    
    author_uid: str
    created: datetime    
    resolved: bool
    number_of_comments: int
    deleted: bool

    owner: User
    replies: List[CommentBase] = []
    class Config:
        orm_mode = True


class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    comment_uid: int    
    created: datetime    
    deleted: bool

    owner: User
    post: Request
    class Config:
        orm_mode = True