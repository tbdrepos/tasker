import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root(client: AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Tasker API"


@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient) -> None:
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "alice@example.com",
            "username": "alice",
            "password": "securepass",
        },
    )
    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/v1/auth/login",
        data={"username": "alice@example.com", "password": "securepass"},
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
