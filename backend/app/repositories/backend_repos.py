from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import RepositoryModel, FileModel, CommitModel, TechnicalDebtModel, TimelineEventModel, DependencyModel
from typing import List, Optional

class RepoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, repo: RepositoryModel) -> RepositoryModel:
        self.db.add(repo)
        await self.db.commit()
        await self.db.refresh(repo)
        return repo

    async def get_by_id(self, repo_id: int) -> Optional[RepositoryModel]:
        result = await self.db.execute(select(RepositoryModel).filter(RepositoryModel.id == repo_id))
        return result.scalars().first()

    async def get_by_path(self, path: str) -> Optional[RepositoryModel]:
        result = await self.db.execute(select(RepositoryModel).filter(RepositoryModel.path == path))
        return result.scalars().first()

    async def list_all(self) -> List[RepositoryModel]:
        result = await self.db.execute(select(RepositoryModel))
        return result.scalars().all()

class FileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_repo(self, repo_id: int) -> List[FileModel]:
        result = await self.db.execute(select(FileModel).filter(FileModel.repo_id == repo_id))
        return result.scalars().all()

class DebtRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_repo(self, repo_id: int) -> List[TechnicalDebtModel]:
        result = await self.db.execute(select(TechnicalDebtModel).filter(TechnicalDebtModel.repo_id == repo_id))
        return result.scalars().all()
