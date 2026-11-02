import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_board(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    response = await client.post(
        "/api/v1/boards",
        json={"title": "Sprint 1", "description": "Q1 goals"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Sprint 1"
