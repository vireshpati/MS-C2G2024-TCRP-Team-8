from sqlalchemy.orm import Session #
from fastapi import APIRouter, Depends, HTTPException, Query
# from app.dependencies import get_current_user
# from app.services.firebase_service import db
from sql_app.schemas import *
import logging
from datetime import datetime

from . import models, schemas

router = APIRouter()

@router.post("/bulletin", response_model=schemas.Request)
def create_request(
    request: RequestCreate,
    uid: str # fix this = Depends(get_current_user)
):
    try:
        logging.info(f"Creating request for uid: {uid}")
        request.author_uid = uid
        doc_ref = db.collection('requests').add(request.dict())
        logging.info("Request created successfully.")
        return request
    except Exception as e:
        logging.error(f"Error in create_request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/bulletin/{post_uid}", response_model=Comment)
def create_comment(
    comment: CommentCreate,
    uid: str # = Depends(get_current_user)
):
    try:
        logging.info(f"Creating comment for post_uid: {comment.post_uid}")
        comment.author_uid = uid
        doc_ref = db.collection('comments').add(comment.dict())
        doc_ref = db.collection('requests').document(comment.post_uid)
        doc_ref.update({
            'number_of_comments': firestore.Increment(1)
        })
        logging.info("Comment created successfully.")
        return request
    except Exception as e:
        logging.error(f"Error in create_comment: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/bulletin/{post_uid}", response_model=Request)
async def get_request_comments(post_uid: int):
    try:
        logging.info(f"Fetching request with post_uid: {post_uid}")
        doc_ref = db.collection('requests').document(post_uid)
        doc = doc_ref.get()
        if doc.exists:
            replies_ref = doc_ref.collection('replies')
            replies = replies_ref.stream() 
            replies_list = [reply.to_dict() for reply in replies]

            request_data = doc.to_dict()
            request_data['replies'] = replies_list

            logging.info(f"Request data retrieved: {request_data}")
            return Request(**request_data)
        else:
            logging.warning(f"Request post not found for post_uid: {post_uid}")
            raise HTTPException(status_code=404, detail="Request post not found.")
    except Exception as e:
        logging.error(f"Error in get_request_comments: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

VALID_TAGS = ['babysitting', 'tutoring', 'pickupchild', 'mealshare', 'needride', 'others']

@router.get("/bulletin", response_model=Request)
async def get_request_list(
    sort_field: str = Query(None, description="Sort by 'post_creation_date' or 'confirm_by'"),
    asc: bool = Query(False, description="True for ascending order, False (default) for descending order"),
    filter_tag: str = Query(None, description="one of 'babysitting', 'tutoring', 'pickupchild', 'mealshare', 'needride', 'others'"),
    page: int = 1, 
    limit: int = 20,
    resolved_requests: bool = Query(False, description="True shows resolved requests, False (default) shows unresolved requestsr")
):
    try:
        logging.info(f"Fetching bulletin board.")
        doc_ref = db.collection('requests')
        if tag and tag not in VALID_TAGS:
            raise HTTPException(status_code=400, detail=f"Invalid tag: {tag}. Must be one of {VALID_TAGS}.")
        now = datetime.datetime.utcnow()
        offset = (page - 1) * limit

        query = doc_ref.where('deleted', '==', False) \
                        .where('resolved', '==', resolved_requests) \
                        .where('date_help_needed', '>=', now)
        if tag:
            query = query.where('tag', '==', tag)
        if sort_by == 'post_creation_date':
            query = query.order_by('post_creation_date', direction=firestore.Query.ASCENDING if asc else firestore.Query.DESCENDING)
        elif sort_by == 'confirm_by':
            query = query.order_by('confirm_by', direction=firestore.Query.ASCENDING if asc else firestore.Query.DESCENDING)
        elif sort_by == 'date_help_needed':
            query = query.order_by('date_help_needed', direction=firestore.Query.ASCENDING if asc else firestore.Query.DESCENDING)
        else:
            query = query.order_by('post_creation_date', direction=firestore.Query.DESCENDING)
        relavent_requests = query.limit(limit).offset(offset).stream()

        # Convert to a list of dictionaries
        relavent_requests_list = [req.to_dict() for req in relavent_requests]
        if not relavent_requests_list:
            logging.warning(f"No relavent posts found")
            raise HTTPException(status_code=404, detail="No relavent posts found on bulletin board")

        # Convert dictionaries to Request instances
        reqs = [Request(**req) for req in relavent_requests_list]
        logging.info(f"Bulletin board retrieved")
        return reqs          
    except Exception as e:
        logging.error(f"Error in get_request_list {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.put("/bulletin/{post_uid}/edit", response_model=schemas.Request)
def edit_request(
    post_uid: str,
    request: RequestCreate,
    uid: str # fix this = Depends(get_current_user)
):
    try:
        logging.info(f"Updating request with post_uid: {post_uid}")
        doc_ref = db.collection('requests').document(post_uid)
        doc = doc_ref.get()
        if not doc:
            raise HTTPException(status_code=404, detail="Request not found")
        doc_data = doc.to_dict()
        if doc_data.get('author_uid') != uid:
            raise HTTPException(status_code=403, detail="User not authorized to edit this request")
        request.created = datetime.utcnow()
        doc_ref.update(request.dict())
        logging.info("Request updated successfully.")
        return request
    except Exception as e:
        logging.error(f"Error in update_request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/bulletin/{post_uid}", response_model=schemas.Request)
def resolve_request(
    post_uid: str,
    uid: str # fix this = Depends(get_current_user)
):
    try:
        logging.info(f"Resolving request post_uid: {post_uid}")
        doc_ref = db.collection('requests').document(post_uid)
        doc = doc_ref.get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Request not found")
        doc_data = doc.to_dict()
        if doc_data.get('author_uid') != uid:
            raise HTTPException(status_code=403, detail="User not authorized to resolve this request")
        doc_ref.update({'resolved': True})
        logging.info("Request resolved successfully.")
        return db.collection('requests').document(post_uid)
    except Exception as e:
        logging.error(f"Error in update_request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/bulletin/{post_id}")
def delete_request(
    post_uid: int,
    uid: str # fix this = Depends(get_current_user)
):
    try:
        logging.info(f"Deleting request for post_uid: {post_uid}")
        if not post_uid:
            raise HTTPException(status_code=400, detail="post_uid is required")
        doc_ref = db.collection('requests').document(post_uid)
        doc = doc_ref.get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Request not found")
        doc_data = doc.to_dict()
        if doc_data.get('author_uid') != user_uid:
            raise HTTPException(status_code=403, detail="User not authorized to delete this post")
        doc_ref.delete()
        logging.info("Request of post_uid: {post_uid} deleted successfully.")
        return request
    except Exception as e:
        logging.error(f"Error in create_request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")