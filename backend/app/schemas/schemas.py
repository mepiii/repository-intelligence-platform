from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class RepositoryCreate(BaseModel):
    name: str
    path: str
    url: Optional[str] = None
    default_branch: str = "main"

class RepositoryResponse(BaseModel):
    id: int
    name: str
    path: str
    url: Optional[str]
    default_branch: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SymbolResponse(BaseModel):
    id: int
    name: str
    kind: str
    start_line: int
    end_line: int
    docstring: Optional[str] = None
    signature: Optional[str] = None

    class Config:
        from_attributes = True

class FileResponse(BaseModel):
    id: int
    path: str
    language: str
    size: int
    line_count: int
    symbols: List[SymbolResponse] = []

    class Config:
        from_attributes = True

class SearchResult(BaseModel):
    file_path: str
    entity_type: str
    content_snippet: str
    score: float
    metadata: Dict[str, Any] = {}

class GraphNode(BaseModel):
    id: str
    label: str
    name: str
    type: str
    properties: Dict[str, Any] = {}

class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    label: str

class KnowledgeGraphResponse(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]

class DebtIssue(BaseModel):
    rule: str
    message: str
    severity: str # high, medium, low
    line: Optional[int] = None

class TechnicalDebtResponse(BaseModel):
    repo_id: int
    overall_debt_score: float
    overall_maintainability_score: float
    file_reports: List[Dict[str, Any]]
    suggestions: List[str]

class TimelineEventResponse(BaseModel):
    id: int
    event_type: str
    description: str
    timestamp: datetime
    metadata_json: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    repo_id: int
    message: str
    provider: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    citations: List[Dict[str, Any]] = []
    reasoning_steps: List[str] = []
