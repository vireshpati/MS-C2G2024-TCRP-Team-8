from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.fcm_messaging import store_fcm_token, send_message_to_user

router = APIRouter()

class TokenRequest(BaseModel):
    userId: str
    token: str

@router.post("/store-token")
def store_token(request: TokenRequest):
    user_id = request.userId
    fcm_token = request.token
    
    if user_id and fcm_token:
        store_fcm_token(user_id, fcm_token)
        return {"message": "Token stored successfully."}
    raise HTTPException(status_code=400, detail="User ID and token are required.")

class MessageRequest(BaseModel):
    userId: str
    message: str

@router.post("/send-message")
def send_message(request: MessageRequest):
    user_id = request.userId
    message = request.message

    result = send_message_to_user(user_id, message)
    
    if result:
        return {"message": "Message sent successfully."}
    raise HTTPException(status_code=500, detail="Failed to send message.")