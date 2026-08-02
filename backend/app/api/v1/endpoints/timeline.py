from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.session import get_db
from app.db.models import CommitModel, DependencyModel
from app.schemas.schemas import TimelineEventResponse
from app.services.timeline.timeline_service import TimelineService

router = APIRouter()

@router.get("", response_model=List[TimelineEventResponse])
async def get_timeline(repo_id: int = Query(1), db: AsyncSession = Depends(get_db)):
    c_res = await db.execute(select(CommitModel).filter(CommitModel.repo_id == repo_id))
    commits_models = c_res.scalars().all()
    commits = [{
        "hash": c.hash,
        "author_name": c.author_name,
        "author_email": c.author_email,
        "commit_date": c.commit_date,
        "message": c.message
    } for c in commits_models]

    d_res = await db.execute(select(DependencyModel).filter(DependencyModel.repo_id == repo_id))
    deps_models = d_res.scalars().all()
    deps = [{
        "name": d.name,
        "version": d.version,
        "source_file": d.source_file
    } for d in deps_models]

    raw_events = TimelineService.generate_timeline(commits, deps, tags=["v1.0.0"])

    res = []
    for idx, e in enumerate(raw_events):
        res.append(TimelineEventResponse(
            id=idx + 1,
            event_type=e["event_type"],
            description=e["description"],
            timestamp=e["timestamp"],
            metadata_json=e["metadata_json"]
        ))

    return res
