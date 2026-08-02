import math
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import EmbeddingModel
from app.core.config import settings

class VectorService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self._model = None

    def _get_model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(settings.EMBEDDING_MODEL)
            except Exception:
                self._model = "mock"
        return self._model

    def encode(self, text: str) -> List[float]:
        model = self._get_model()
        if model != "mock":
            try:
                emb = model.encode(text)
                return emb.tolist()
            except Exception:
                pass
        # Pseudo vector for fallback (length 384)
        hash_val = sum(ord(c) for c in text)
        return [math.sin(hash_val + i) * 0.1 for i in range(384)]

    async def index_content(self, repo_id: int, entity_type: str, entity_id: str, content: str):
        vec = self.encode(content)
        embedding_obj = EmbeddingModel(
            repo_id=repo_id,
            entity_type=entity_type,
            entity_id=entity_id,
            content=content,
            embedding=vec
        )
        self.db.add(embedding_obj)
        await self.db.commit()

    async def search(self, repo_id: int, query: str, top_k: int = 10, search_type: str = "hybrid") -> List[Dict[str, Any]]:
        query_vec = self.encode(query)
        
        # Database query
        result = await self.db.execute(select(EmbeddingModel).filter(EmbeddingModel.repo_id == repo_id))
        records = result.scalars().all()

        results = []
        q_words = set(query.lower().split())

        for rec in records:
            score = 0.0
            content_lower = rec.content.lower()

            # Keyword matching score
            kw_match = sum(1 for w in q_words if w in content_lower)
            kw_score = kw_match / (len(q_words) + 1e-5)

            # Cosine similarity vector score
            vec_score = 0.0
            if rec.embedding is not None and len(rec.embedding) == len(query_vec):
                dot = sum(a * b for a, b in zip(rec.embedding, query_vec))
                norm_a = math.sqrt(sum(a * a for a in rec.embedding))
                norm_b = math.sqrt(sum(b * b for b in query_vec))
                if norm_a > 0 and norm_b > 0:
                    vec_score = dot / (norm_a * norm_b)

            if search_type == "keyword":
                score = kw_score
            elif search_type == "semantic":
                score = vec_score
            else: # hybrid
                score = (0.6 * vec_score) + (0.4 * kw_score)

            if score > 0.05:
                results.append({
                    "file_path": rec.entity_id,
                    "entity_type": rec.entity_type,
                    "content_snippet": rec.content[:300],
                    "score": round(score, 4),
                    "metadata": {"repo_id": repo_id}
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
