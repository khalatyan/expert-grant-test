import pytest
from httpx import AsyncClient
from httpx import ASGITransport

from main import app, init_db


@pytest.mark.asyncio
async def test_posts_filtering():
    await init_db()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/posts?category=tech&keywords=python")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] >= 1
        assert "python" in data["posts"][0]["word_freq"]
