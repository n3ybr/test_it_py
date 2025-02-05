import pytest
from httpx import AsyncClient, ASGITransport

from main import app

@pytest.mark.asyncio
async def test_get_category():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/categories/2") 

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 4
    assert data[0]["name"] == "Смартфоны"
    assert data[1]["name"] == "Аксессуары"
    assert data[2]["name"] == "Чехлы"
    assert data[3]["name"] == "Зарядки"
