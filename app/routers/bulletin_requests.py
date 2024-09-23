from fastapi import APIRouter, Depends, HTTPException, Query
from app.dependencies import get_current_user
from app.models.user import User
from app.models.bulletin_request import Request, Comment
from app.services.bulletin_service import BulletinService
from app.models.patch import ProfilePatch
import logging
from datetime import datetime

router = APIRouter()
firestore_service = FirestoreService()

@router.post("/bulletin", response_model=Request)
def create_request(request: Request):
    try:
        logging.info("Creating request")
        request.created = datetime.utcnow()
        bulletin_service.create_request_post(request.dict())
        return request
    except Exception as e:
        logging.error(f"Error in create_request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/bulletin/{post_uid}/comments", response_model=Comment)
def create_comment(comment: Comment):
    try:
        logging.info(f"Creating comment for post_uid: {comment.post_uid}")
        comment.created = datetime.utcnow()
        bulletin_service.create_comment_reply(comment.post_uid)
        logging.info("Comment created successfully.")
        return comment
    except Exception as e:
        logging.error(f"Error in create_comment: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/bulletin/{post_uid}", response_model=Request)
async def get_request(post_uid: int):
    try:
        logging.info(f"Fetching request with post_uid: {post_uid}")
        request_data = bulletin_service.get_request_post(post_uid)
        if request_data:
            return Request(**request_data)
        else:
            raise HTTPException(status_code=404, detail="Request post not found.")
    except Exception as e:
        logging.error(f"Error in get_request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/bulletin/{post_uid}/comments", response_model=Request)
async def get_comments(post_uid: int):
    try:
        logging.info(f"Fetching comments for request with post_uid: {post_uid}")
        comment_data = bulletin_service.get_comment_replies(post_uid)
        if comment_data:
            return [Comment(**data) for data in comment_data]
        else:
            raise HTTPException(status_code=404, detail="Request post not found.")
    except Exception as e:
        logging.error(f"Error in get_comments: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/bulletin", response_model=Request)
async def get_relavent_request_list(page: int = 1, limit: int = 30):
    try:
        logging.info("Fetching bulletin board")
        request_data = bulletin_service.get_relavent_request_list(page, limit)
        if request_data:
            return [Request(**data) for data in request_data]
        else:
            raise HTTPException(status_code=404, detail="Request posts not found.")
    except Exception as e:
        logging.error(f"Error in get_relavent_request_list: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.put("/bulletin/{post_uid}", response_model=schemas.Request)
def update_request(request: Request):
    try:
        logging.info(f"Updating request with post_uid: {request.post_uid}")
        bulletin_service.update_request_post(request.dict())
        return request
    except Exception as e:
        logging.error(f"Error in update_profile: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/bulletin/{post_uid}/resolve", response_model=schemas.Request)
def resolve_request(post_uid: str):
    try:
        logging.info(f"Toggling request resolved status for post_uid: {post_uid}")    
        toggled_request = bulletin_service.toggle_request_resolved_status(post_uid)
        if toggled_request:
            logging.info("Request resolved status toggled successfully.")
            return toggled_request
        else:
            raise HTTPException(status_code=500, detail="Error toggling resolved status")
    except Exception as e:
        logging.error(f"Error toggling active status for UID: {request.target_uid}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/bulletin/{post_id}")
def delete_request(post_uid: int):
    try:
        logging.info(f"Deleting request for post_uid: {post_uid}")
        bulletin_service.delete_request_post(post_uid)
        return {"message": "Request deleted successfully"}
    except Exception as e:
        logging.error(f"Error in delete_request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")