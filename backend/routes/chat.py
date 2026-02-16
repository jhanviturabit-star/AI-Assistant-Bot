# backend/routes/chat.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import HTTPBearer
from backend.context import current_token
from backend import agent
# from backend.db.redis_client import save_message, get_history
from backend.auth import get_current_user

router = APIRouter(prefix="/chat", tags=["chat"])
security = HTTPBearer()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    message: str

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(chat: ChatRequest, credentials = Depends(security)):
    """Handle chat messages via AI assistant"""
    raw_token = credentials.credentials
    if raw_token.startswith("Bearer "):
        raw_token = raw_token.replace("Bearer ", "")

    current_token.set(raw_token)
    user = get_current_user(token=raw_token)  # reuse Project1 auth logic

    # # Save user message in Redis
    # save_message(user.id, "user", chat.message)

    # Pass message to your agent
    try:
        response = agent.invoke({
            "messages": [
                {"role": "user", "content": chat.message}
            ]
        })
        assistant_msg = response["messages"][-1].content

        # # Save AI response in Redis
        # save_message(user.id, "assistant", assistant_msg)

        return ChatResponse(message=assistant_msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
