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
def create_request(
    uid: str = Depends(get_current_user),
    request: RequestCreate):
    try:
        logging.info(f"Creating request for uid: {uid}")
        request.author_uid = uid
        bulletin_service.create_request_post(uid, request.dict())
        return request
    except Exception as e:
        logging.error(f"Error in create_request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/bulletin/{post_uid}", response_model=Comment)
def create_comment(
    uid: str = Depends(get_current_user),
    comment: CommentCreate):
    try:
        logging.info(f"Creating comment for post_uid: {comment.post_uid}")
        comment.author_uid = uid
        bulletin_service.create_comment_reply(uid, comment.post_uid)

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

# done
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
        logging.info(f"Fetching request with post_uid: {post_uid}")
        request_data = bulletin_service.get_request_post(post_uid)
        if request_data:
            return Request(**request_data)
        else:
            raise HTTPException(status_code=404, detail="Request post not found.")
    except Exception as e:
        logging.error(f"Error in get_request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/bulletin", response_model=Request)
async def get_relavent_request_list(
    sort_field: str = Query(None, description="Sort by 'post_creation_date' or 'confirm_by'"),
    asc: bool = Query(False, description="True for ascending order, False (default) for descending order"),
    filter_tag: str = Query(None, description="one of 'babysitting', 'tutoring', 'pickupchild', 'mealshare', 'needride', 'others'"),
    page: int = 1, 
    limit: int = 20,
    resolved_requests: bool = Query(False, description="True shows resolved requests, False (default) shows unresolved requestsr")
):
    try:
        logging.info(f"Fetching bulletin board")
        request_data = bulletin_service.get_relavent_request_list()
        if request_data:
            return Request(**request_data)
        else:
            raise HTTPException(status_code=404, detail="Request post not found.")
    except Exception as e:
        logging.error(f"Error in get_request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.put("/bulletin/{post_uid}/edit", response_model=schemas.Request)
def update_request(post_uid: str,request: Request):
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

# done
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

# done
@router.delete("/bulletin/{post_id}")
def delete_request(post_uid: int):
    try:
        logging.info(f"Deleting request for post_uid: {post_uid}")
        bulletin_service.delete_request_post(post_uid)
        return {"message": "Request deleted successfully"}
    except Exception as e:
        logging.error(f"Error in delete_request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")