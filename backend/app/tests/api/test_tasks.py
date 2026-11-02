import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_and_list_tasks(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    create_response = await client.post(
        "/api/v1/tasks",
        json={"title": "Write tests", "priority": "important", "status": "todo"},
        headers=auth_headers,
    )
    assert create_response.status_code == 201
    task = create_response.json()
    assert task["title"] == "Write tests"

    list_response = await client.get("/api/v1/tasks", headers=auth_headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
