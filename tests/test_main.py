# tests/test_main.py — A basic test to verify the API starts up correctly
# Run with: pytest tests/

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_health_check():
    """Test that the root endpoint returns a healthy status."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
