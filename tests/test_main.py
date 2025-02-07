import pytest
from httpx import AsyncClient, ASGITransport

from main import app

@pytest.mark.asyncio
async def test_add_category():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        ac.headers["Authorization"] =  "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0MiIsImV4cCI6MTczODkyMjQwN30.Ac924m_S6P7eLpcnRA6rKc_0Y0e99G5PTUxaUupqNqw"
        response = await ac.post("categories/?name=Офисная&parent_id=39") 

    assert response.status_code == 200
    data = response.json()

    assert data['id'] != None

@pytest.mark.asyncio
async def test_get_category():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        ac.headers["Authorization"] =  "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0MiIsImV4cCI6MTczODkyMjQwN30.Ac924m_S6P7eLpcnRA6rKc_0Y0e99G5PTUxaUupqNqw"
        response = await ac.get("/categories/39") 

    assert response.status_code == 200
    data = response.json()

    assert data != None

@pytest.mark.asyncio
async def test_add_rcategory():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        ac.headers["Authorization"] =  "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0MiIsImV4cCI6MTczODkyMjQwN30.Ac924m_S6P7eLpcnRA6rKc_0Y0e99G5PTUxaUupqNqw"
        response = await ac.post("categories/?name=Книги") 

    assert response.status_code == 200
    data = response.json()

    assert data['id'] != None

@pytest.mark.asyncio
async def test_update_category():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        ac.headers["Authorization"] =  "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0MiIsImV4cCI6MTczODkyMjQwN30.Ac924m_S6P7eLpcnRA6rKc_0Y0e99G5PTUxaUupqNqw"
        response = await ac.put("categories/39?name=Новая электроника") 

    assert response.status_code == 200
    data = response.json()

    assert data['id'] != None

@pytest.mark.asyncio
async def test_delete_category():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        ac.headers["Authorization"] =  "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0MiIsImV4cCI6MTczODkyMjQwN30.Ac924m_S6P7eLpcnRA6rKc_0Y0e99G5PTUxaUupqNqw"
        response = await ac.delete("categories/39") 

    assert response.status_code == 200
    data = response.json()

    assert data['id'] != None

@pytest.mark.asyncio
async def test_get_token():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("token", data = {"username": "test2", "password":"Qazwsx12"}) 

    assert response.status_code == 200
    

@pytest.mark.asyncio
async def test_add_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        ac.headers["Authorization"] =  "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0MiIsImV4cCI6MTczODkyMjQwN30.Ac924m_S6P7eLpcnRA6rKc_0Y0e99G5PTUxaUupqNqw"
        response = await ac.post("/users/add/", json={"username": "admin", "password": "Qazwsx12"})

    assert response.status_code == 200
    data = response.json()

    assert data['username'] != None

@pytest.mark.asyncio
async def test_get_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        ac.headers["Authorization"] =  "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0MiIsImV4cCI6MTczODkyMjQwN30.Ac924m_S6P7eLpcnRA6rKc_0Y0e99G5PTUxaUupqNqw"
        response = await ac.get("users/34") 

    assert response.status_code == 200
    data = response.json()

    assert data['username'] != None


@pytest.mark.asyncio
async def test_update_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        ac.headers["Authorization"] =  "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0MiIsImV4cCI6MTczODkyMjQwN30.Ac924m_S6P7eLpcnRA6rKc_0Y0e99G5PTUxaUupqNqw"

        response = await ac.put("users/34?new_password=Qazwsx1113") 

    assert response.status_code == 200
    data = response.json()

    assert data['user_id'] != None

@pytest.mark.asyncio
async def test_delete_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        ac.headers["Authorization"] =  "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0MiIsImV4cCI6MTczODkyMjQwN30.Ac924m_S6P7eLpcnRA6rKc_0Y0e99G5PTUxaUupqNqw"
        response = await ac.delete("users/34") 

    assert response.status_code == 200
    data = response.json()

    assert data['user_id'] != None
