from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.schemas import ChatRequest, ChatResponse
from app.services.assistant.assistant_service import AssistantService

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def assistant_chat(req: ChatRequest, db: AsyncSession = Depends(get_db)):
    service = AssistantService(db)
    res = await service.ask(req.repo_id, req.message, req.provider)
    return ChatResponse(**res)
