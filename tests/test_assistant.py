import pytest
from app.services.assistant.assistant_service import MockLLMProvider

@pytest.mark.asyncio
async def test_mock_llm_provider():
    provider = MockLLMProvider()
    resp = await provider.generate_response("Explain authentication system", "context")
    assert "Authentication" in resp
