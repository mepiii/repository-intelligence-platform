from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import os

from app.db.session import get_db
from app.db.models import RepositoryModel, FileModel, CommitModel, DeveloperModel, DependencyModel, SymbolModel
from app.schemas.schemas import RepositoryCreate, RepositoryResponse
from app.services.scanner.git_scanner import GitScanner
from app.services.intelligence.ast_parser import ASTParser
from app.services.intelligence.symbol_indexer import SymbolIndexer
from app.services.embeddings.vector_service import VectorService
from app.services.graph.neo4j_service import graph_service
from app.services.debt.debt_analyzer import DebtAnalyzer
from app.repositories.backend_repos import RepoRepository

router = APIRouter()

@router.post("", response_model=RepositoryResponse)
async def create_repository(repo_in: RepositoryCreate, db: AsyncSession = Depends(get_db)):
    repo_repo = RepoRepository(db)
    existing = await repo_repo.get_by_path(repo_in.path)
    if existing:
        return existing
    
    new_repo = RepositoryModel(
        name=repo_in.name,
        path=repo_in.path,
        url=repo_in.url,
        default_branch=repo_in.default_branch
    )
    return await repo_repo.create(new_repo)

@router.get("", response_model=List[RepositoryResponse])
async def list_repositories(db: AsyncSession = Depends(get_db)):
    repo_repo = RepoRepository(db)
    return await repo_repo.list_all()

@router.post("/{repo_id}/scan")
async def scan_repository(repo_id: int, db: AsyncSession = Depends(get_db)):
    repo_repo = RepoRepository(db)
    repo = await repo_repo.get_by_id(repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    scanner = GitScanner(repo.path)
    scan_res = scanner.scan()

    # Save Commits
    for c in scan_res["commits"]:
        commit_obj = CommitModel(
            repo_id=repo.id,
            hash=c["hash"],
            author_name=c["author_name"],
            author_email=c["author_email"],
            commit_date=c["commit_date"],
            message=c["message"]
        )
        db.add(commit_obj)

    # Save Files & Symbols
    symbols_map = {}
    for f in scan_res["files"]:
        file_obj = FileModel(
            repo_id=repo.id,
            path=f["path"],
            language=f["language"],
            size=f["size"],
            line_count=f["line_count"],
            content=f["content"]
        )
        db.add(file_obj)
        await db.flush()

        parsed = ASTParser.parse_file(f["content"], f["language"], f["path"])
        symbols_map[f["path"]] = parsed["symbols"]

        for s in parsed["symbols"]:
            sym_obj = SymbolModel(
                file_id=file_obj.id,
                name=s["name"],
                kind=s["kind"],
                start_line=s["start_line"],
                end_line=s["end_line"],
                docstring=s["docstring"],
                signature=s["signature"]
            )
            db.add(sym_obj)

    # Save Dependencies
    for d in scan_res["dependencies"]:
        dep_obj = DependencyModel(
            repo_id=repo.id,
            name=d["name"],
            version=d.get("version"),
            source_file=d.get("source_file", "manifest"),
            dep_type=d.get("type", "runtime")
        )
        db.add(dep_obj)

    await db.commit()

    # Build Knowledge Graph
    graph_service.build_graph_from_repo_data(
        repo.id,
        repo.name,
        scan_res["files"],
        scan_res["commits"],
        symbols_map
    )

    return {"status": "scanned", "files_scanned": len(scan_res["files"]), "commits": len(scan_res["commits"])}

@router.post("/{repo_id}/index")
async def index_repository(repo_id: int, db: AsyncSession = Depends(get_db)):
    repo_repo = RepoRepository(db)
    repo = await repo_repo.get_by_id(repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    vector_service = VectorService(db)
    scanner = GitScanner(repo.path)
    scan_res = scanner.scan()

    indexed_count = 0
    for f in scan_res["files"]:
        if f["content"]:
            await vector_service.index_content(repo.id, "code", f["path"], f["content"])
            indexed_count += 1

    for d in scan_res["docs"]:
        if d["content"]:
            await vector_service.index_content(repo.id, "doc", d["path"], d["content"])
            indexed_count += 1

    return {"status": "indexed", "total_vectors": indexed_count}
