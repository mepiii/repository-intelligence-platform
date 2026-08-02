from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.schemas.schemas import SearchResult
from app.services.embeddings.vector_service import VectorService

router = APIRouter()

@router.get("", response_model=List[SearchResult])
async def search_repository(
    repo_id: int = Query(1),
    q: str = Query(...),
    type: str = Query("hybrid"),
    db: AsyncSession = Depends(get_db)
):
    vector_service = VectorService(db)
    return await vector_service.search(repo_id, q, top_k=10, search_type=type)
