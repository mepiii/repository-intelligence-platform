from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON, Boolean
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class RepositoryModel(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_order=True, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    path = Column(String(1024), nullable=False, unique=True)
    url = Column(String(1024), nullable=True)
    default_branch = Column(String(255), default="main")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    commits = relationship("CommitModel", back_populates="repository", cascade="all, delete-orphan")
    files = relationship("FileModel", back_populates="repository", cascade="all, delete-orphan")
    dependencies = relationship("DependencyModel", back_populates="repository", cascade="all, delete-orphan")
    debts = relationship("TechnicalDebtModel", back_populates="repository", cascade="all, delete-orphan")
    timeline_events = relationship("TimelineEventModel", back_populates="repository", cascade="all, delete-orphan")

class DeveloperModel(Base):
    __tablename__ = "developers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    commits = relationship("CommitModel", back_populates="developer")

class CommitModel(Base):
    __tablename__ = "commits"

    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, ForeignKey("repositories.id"), nullable=False)
    hash = Column(String(64), nullable=False, index=True)
    developer_id = Column(Integer, ForeignKey("developers.id"), nullable=True)
    author_name = Column(String(255), nullable=False)
    author_email = Column(String(255), nullable=False)
    commit_date = Column(DateTime, nullable=False)
    message = Column(Text, nullable=False)

    repository = relationship("RepositoryModel", back_populates="commits")
    developer = relationship("DeveloperModel", back_populates="commits")

class FileModel(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, ForeignKey("repositories.id"), nullable=False)
    path = Column(String(1024), nullable=False)
    language = Column(String(50), nullable=False)
    size = Column(Integer, default=0)
    line_count = Column(Integer, default=0)
    content = Column(Text, nullable=True)

    repository = relationship("RepositoryModel", back_populates="files")
    symbols = relationship("SymbolModel", back_populates="file", cascade="all, delete-orphan")

class SymbolModel(Base):
    __tablename__ = "symbols"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False)
    name = Column(String(255), nullable=False, index=True)
    kind = Column(String(50), nullable=False) # function, class, method, import
    start_line = Column(Integer, nullable=False)
    end_line = Column(Integer, nullable=False)
    docstring = Column(Text, nullable=True)
    signature = Column(Text, nullable=True)

    file = relationship("FileModel", back_populates="symbols")

class EmbeddingModel(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, ForeignKey("repositories.id"), nullable=False)
    entity_type = Column(String(50), nullable=False) # code, doc, commit
    entity_id = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(384), nullable=True)

class DependencyModel(Base):
    __tablename__ = "dependencies"

    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, ForeignKey("repositories.id"), nullable=False)
    name = Column(String(255), nullable=False)
    version = Column(String(100), nullable=True)
    source_file = Column(String(255), nullable=False)
    dep_type = Column(String(50), default="runtime") # runtime, dev

    repository = relationship("RepositoryModel", back_populates="dependencies")

class TechnicalDebtModel(Base):
    __tablename__ = "technical_debt"

    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, ForeignKey("repositories.id"), nullable=False)
    file_path = Column(String(1024), nullable=False)
    debt_score = Column(Float, nullable=False)
    maintainability_score = Column(Float, nullable=False)
    issues = Column(JSON, nullable=False)
    suggestions = Column(JSON, nullable=False)

    repository = relationship("RepositoryModel", back_populates="debts")

class TimelineEventModel(Base):
    __tablename__ = "timeline_events"

    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, ForeignKey("repositories.id"), nullable=False)
    event_type = Column(String(50), nullable=False) # commit, release, dep_add, dep_remove, refactor
    description = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    metadata_json = Column(JSON, nullable=True)

    repository = relationship("RepositoryModel", back_populates="timeline_events")
