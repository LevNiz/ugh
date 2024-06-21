import pytest
from httpx import AsyncClient
from fastapi import status
from app.main import app
from app.database import database

@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

@pytest.fixture(scope="module", autouse=True)
async def setup_and_teardown():
    await database.connect()
    yield
    await database.disconnect()

@pytest.mark.asyncio
async def test_register_user(async_client: AsyncClient):
    response = await async_client.post("/register/", json={
        "email": "testuser@example.com",
        "pass_": "testpassword"
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "User created successfully"}

@pytest.mark.asyncio
async def test_login_user(async_client: AsyncClient):
    # Register user first
    await async_client.post("/register/", json={
        "email": "testuser@example.com",
        "pass_": "testpassword"
    })
    # Login
    response = await async_client.post("/token", data={
        "username": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_get_current_user(async_client: AsyncClient):
    # Register and login user first
    await async_client.post("/register/", json={
        "email": "testuser@example.com",
        "pass_": "testpassword"
    })
    login_response = await async_client.post("/token", data={
        "username": "testuser@example.com",
        "password": "testpassword"
    })
    access_token = login_response.json()["access_token"]
    
    # Get current user
    response = await async_client.get("/users/me/", headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "testuser@example.com"
