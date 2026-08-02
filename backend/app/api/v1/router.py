from fastapi import APIRouter
from app.api.v1.endpoints import repositories, search, graph, timeline, debt, assistant, health

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(repositories.router, prefix="/repositories", tags=["Repositories"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(graph.router, prefix="/graph", tags=["Knowledge Graph"])
api_router.include_router(timeline.router, prefix="/timeline", tags=["Timeline"])
api_router.include_router(debt.router, prefix="/technical-debt", tags=["Technical Debt"])
api_router.include_router(assistant.router, prefix="/assistant", tags=["AI Assistant"])
