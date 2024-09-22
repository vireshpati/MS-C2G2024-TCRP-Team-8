from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date, CheckConstraint
from sqlalchemy.orm import relationship
import datetime

from .database import Base

class Users(Base):
    __tablename__ = "users"     # table name

    uid = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

    posts = relationship("Requests", back_populates="owner")
    replies = relationship("Comments", back_populates="owner")

class Requests(Base):
    __tablename__ = "requests"

    post_uid = Column(Integer, primary_key=True)
    author_uid = Column(Integer) #, ForeignKey(Users.uid))  # fix this
    title = Column(String)
    content = Column(String)
    tag = Column(String, default='others')
    created = Column(DateTime, default=datetime.datetime.utcnow)
    location_of_help = Column(String)
    date_help_needed = Column(Date)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    confirm_by = Column(DateTime)
    resolved = Column(Boolean, default=False)
    number_of_comments = Column(Integer, default=0)
    deleted = Column(Boolean, default=False)

    __table_args__ = (
        CheckConstraint(
            "tag IN ('babysitting', 'tutoring', 'pickupchild', 'mealshare', 'needride', 'others')",
            name="check_tag"
        ),
    )

    owner = relationship("Users", back_populates="posts")
    replies = relationship("Comments", back_populates="posts")

class Comments(Base):
    __tablename__ = "comments"

    comment_uid = Column(Integer, primary_key=True)
    post_uid = Column(Integer) #, ForeignKey("Requests.post_uid"))
    author_uid = Column(Integer, ForeignKey(Users.uid))  # fix this
    content = Column(String) # TEXT NOT NULL,
    created = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("Users", back_populates="replies")
    post = relationship("Requests", back_populates="replies")
