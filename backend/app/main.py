import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.api.v1.router import api_router
from app.db.base import Base
from app.db.session import engine, AsyncSessionLocal
from app.db.models import RepositoryModel
from app.services.scanner.git_scanner import GitScanner
from app.services.intelligence.ast_parser import ASTParser
from app.services.embeddings.vector_service import VectorService
from app.services.graph.neo4j_service import graph_service
from app.db.models import FileModel, CommitModel, SymbolModel, DependencyModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Initializing Database Tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Auto index sample repository on launch
    if settings.AUTO_INDEX_SAMPLE:
        logger.info("Auto-indexing sample repository...")
        sample_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../examples/sample_repo"))
        if os.path.exists(sample_path):
            async with AsyncSessionLocal() as db:
                from app.repositories.backend_repos import RepoRepository
                repo_repo = RepoRepository(db)
                existing = await repo_repo.get_by_path(sample_path)
                if not existing:
                    repo_obj = RepositoryModel(name="Sample Project", path=sample_path, url="https://github.com/example/sample-repo")
                    repo_obj = await repo_repo.create(repo_obj)
                    
                    scanner = GitScanner(sample_path)
                    scan_res = scanner.scan()
                    vector_svc = VectorService(db)

                    symbols_map = {}
                    for f in scan_res["files"]:
                        fm = FileModel(repo_id=repo_obj.id, path=f["path"], language=f["language"], size=f["size"], line_count=f["line_count"], content=f["content"])
                        db.add(fm)
                        await db.flush()
                        
                        parsed = ASTParser.parse_file(f["content"], f["language"], f["path"])
                        symbols_map[f["path"]] = parsed["symbols"]
                        for s in parsed["symbols"]:
                            db.add(SymbolModel(file_id=fm.id, name=s["name"], kind=s["kind"], start_line=s["start_line"], end_line=s["end_line"], docstring=s["docstring"], signature=s["signature"]))

                        if f["content"]:
                            await vector_svc.index_content(repo_obj.id, "code", f["path"], f["content"])

                    for c in scan_res["commits"]:
                        db.add(CommitModel(repo_id=repo_obj.id, hash=c["hash"], author_name=c["author_name"], author_email=c["author_email"], commit_date=c["commit_date"], message=c["message"]))

                    for d in scan_res["dependencies"]:
                        db.add(DependencyModel(repo_id=repo_obj.id, name=d["name"], version=d.get("version"), source_file=d.get("source_file", "manifest"), dep_type=d.get("type", "runtime")))

                    await db.commit()
                    graph_service.build_graph_from_repo_data(repo_obj.id, repo_obj.name, scan_res["files"], scan_res["commits"], symbols_map)
                    logger.info("Sample repository indexed successfully!")

    yield
    logger.info("Shutting down...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
