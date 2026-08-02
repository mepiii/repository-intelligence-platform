from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.db.models import FileModel, SymbolModel
from app.schemas.schemas import TechnicalDebtResponse
from app.services.debt.debt_analyzer import DebtAnalyzer
from app.services.intelligence.ast_parser import ASTParser

router = APIRouter()

@router.get("", response_model=TechnicalDebtResponse)
async def get_technical_debt(repo_id: int = Query(1), db: AsyncSession = Depends(get_db)):
    f_res = await db.execute(select(FileModel).filter(FileModel.repo_id == repo_id))
    files_models = f_res.scalars().all()
    
    files = []
    symbols_map = {}
    for f in files_models:
        files.append({"path": f.path, "content": f.content or "", "language": f.language})
        parsed = ASTParser.parse_file(f.content or "", f.language, f.path)
        symbols_map[f.path] = parsed["symbols"]

    analysis = DebtAnalyzer.analyze_repository(files, symbols_map)
    return TechnicalDebtResponse(
        repo_id=repo_id,
        overall_debt_score=analysis["overall_debt_score"],
        overall_maintainability_score=analysis["overall_maintainability_score"],
        file_reports=analysis["file_reports"],
        suggestions=analysis["suggestions"]
    )
