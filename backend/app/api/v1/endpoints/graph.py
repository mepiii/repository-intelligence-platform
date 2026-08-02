from fastapi import APIRouter, Query
from app.schemas.schemas import KnowledgeGraphResponse
from app.services.graph.neo4j_service import graph_service

router = APIRouter()

@router.get("", response_model=KnowledgeGraphResponse)
async def get_graph(repo_id: int = Query(1)):
    data = graph_service.get_graph_data()
    return data
