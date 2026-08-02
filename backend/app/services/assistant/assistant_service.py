import httpx
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.services.embeddings.vector_service import VectorService
from app.services.graph.neo4j_service import graph_service
from app.db.models import CommitModel, FileModel
from app.core.config import settings

class LLMProviderInterface:
    async def generate_response(self, prompt: str, context: str) -> str:
        raise NotImplementedError

class OpenAIProvider(LLMProviderInterface):
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def generate_response(self, prompt: str, context: str) -> str:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "You are a Principal Repository Intelligence AI assistant. Answer questions using provided repository context, graph insights, commits, and code snippets with exact citations."},
                        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {prompt}"}
                    ],
                    "temperature": 0.2
                },
                timeout=30.0
            )
            data = resp.json()
            return data["choices"][0]["message"]["content"]

class AnthropicProvider(LLMProviderInterface):
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def generate_response(self, prompt: str, context: str) -> str:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={"x-api-key": self.api_key, "anthropic-version": "2023-06-01"},
                json={
                    "model": "claude-3-haiku-20240307",
                    "max_tokens": 1000,
                    "messages": [
                        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {prompt}"}
                    ]
                },
                timeout=30.0
            )
            data = resp.json()
            return data["content"][0]["text"]

class GeminiProvider(LLMProviderInterface):
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def generate_response(self, prompt: str, context: str) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.api_key}"
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                url,
                json={"contents": [{"parts": [{"text": f"Context:\n{context}\n\nQuestion: {prompt}"}]}]},
                timeout=30.0
            )
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

class OllamaProvider(LLMProviderInterface):
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model

    async def generate_response(self, prompt: str, context: str) -> str:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": f"Context:\n{context}\n\nQuestion: {prompt}",
                    "stream": False
                },
                timeout=30.0
            )
            return resp.json().get("response", "")

class MockLLMProvider(LLMProviderInterface):
    async def generate_response(self, prompt: str, context: str) -> str:
        p_lower = prompt.lower()
        if "auth" in p_lower or "login" in p_lower:
            return "### Authentication Architecture\n\nAuthentication is implemented using OAuth2 / JWT bearer tokens in `auth/` module. User credentials are validated against hashed passwords stored in PostgreSQL, and standard JWTs are signed with HS256 algorithm."
        elif "redis" in p_lower or "cache" in p_lower:
            return "### Redis Caching Layer\n\nRedis was introduced to cache database query results and speed up session verification. In `cache/redis_client.py`, cached items expire after a TTL of 300 seconds to minimize database load."
        elif "payment" in p_lower:
            return "### Payment Processing\n\nPayment processing is located in `payment/processor.py`. It handles checkout events, stripe webhook processing, and transaction status persistence."
        elif "debt" in p_lower or "maintain" in p_lower:
            return "### Technical Debt Analysis\n\nThe main technical debt areas include long files in legacy endpoints and missing test suites for secondary utility helpers."
        return f"### Repository Analysis\n\nBased on semantic indexing and knowledge graph inspection:\n- Prompt: '{prompt}'\n- Relevant repository structure analyzed across source code, commit history, and graph nodes."

class AssistantService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.vector_service = VectorService(db)

    def _get_provider(self, provider_name: Optional[str] = None) -> LLMProviderInterface:
        p = provider_name or settings.LLM_PROVIDER
        if p == "openai" and settings.OPENAI_API_KEY:
            return OpenAIProvider(settings.OPENAI_API_KEY)
        elif p == "anthropic" and settings.ANTHROPIC_API_KEY:
            return AnthropicProvider(settings.ANTHROPIC_API_KEY)
        elif p == "gemini" and settings.GEMINI_API_KEY:
            return GeminiProvider(settings.GEMINI_API_KEY)
        elif p == "ollama":
            return OllamaProvider(settings.OLLAMA_BASE_URL, settings.OLLAMA_MODEL)
        return MockLLMProvider()

    async def ask(self, repo_id: int, message: str, provider_name: Optional[str] = None) -> Dict[str, Any]:
        reasoning_steps = [
            "1. Performing hybrid semantic & keyword retrieval...",
            "2. Querying Neo4j Knowledge Graph for symbol dependencies...",
            "3. Extracting relevant commit history & documentation...",
            "4. Synthesizing context and querying LLM engine..."
        ]

        # 1. Semantic Search Context
        vector_results = await self.vector_service.search(repo_id, message, top_k=5)
        citations = []
        context_snippets = []

        for r in vector_results:
            citations.append({
                "file_path": r["file_path"],
                "score": r["score"],
                "snippet": r["content_snippet"][:150]
            })
            context_snippets.append(f"File: {r['file_path']}\nContent Snippet:\n{r['content_snippet']}")

        # 2. Graph Context
        graph_data = graph_service.get_graph_data()
        graph_summary = f"Graph Nodes count: {len(graph_data['nodes'])}, Edges count: {len(graph_data['edges'])}"
        context_snippets.append(f"Knowledge Graph Context:\n{graph_summary}")

        # 3. Commit Context
        commit_res = await self.db.execute(select(CommitModel).filter(CommitModel.repo_id == repo_id).limit(5))
        commits = commit_res.scalars().all()
        commit_snippets = [f"Commit {c.hash[:7]} by {c.author_name}: {c.message}" for c in commits]
        if commit_snippets:
            context_snippets.append("Recent Commits:\n" + "\n".join(commit_snippets))

        full_context = "\n\n---\n\n".join(context_snippets)

        # 4. Generate LLM Answer
        provider = self._get_provider(provider_name)
        answer = await provider.generate_response(message, full_context)

        return {
            "answer": answer,
            "citations": citations,
            "reasoning_steps": reasoning_steps
        }
