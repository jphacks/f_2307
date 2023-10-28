from fastapi import APIRouter, Header, HTTPException

import firebase
from models.friend import Friend
from models.user import User
from models.message import Message

router = APIRouter()

@router.get("/messages/{friend_uid}")
async def get_message(friend_uid: str, authorization: str = Header(None)):
    # 私は誰か
    if authorization is None:
        raise HTTPException(status_code=401)
    try:
        uid = firebase.get_user_uid(authorization)
    except:
        raise HTTPException(status_code=401)
    
    message_list = Message.get_message_list(uid, friend_uid)

    response = []
    for message in message_list:
        response.append(
            {
                "fromUserId": message.from_user_id,
                "message": message.message,
                "createdAt": message.create_at,
            }
        )

    return response
