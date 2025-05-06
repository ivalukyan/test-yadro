import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from fastapi import status

from src.backend.main import app
from src.database.engine import get_db_session
from tests.utils.test_utils import get_test_db_session, init_test_db, drop_test_db

# Подмена зависимости
app.dependency_overrides[get_db_session] = get_test_db_session

sample_graph = {
    "nodes": [
        {"name": "a"},
        {"name": "b"},
        {"name": "c"},
        {"name": "d"}
    ],
    "edges": [
        {"source": "a", "target": "c"},
        {"source": "b", "target": "c"},
        {"source": "c", "target": "d"}
    ]
}


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    drop_test_db()
    init_test_db()
    yield
    drop_test_db()


@pytest.fixture(scope="module")
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_create_graph(async_client):
    response = await async_client.post("/api/graph/", json=sample_graph)
    assert response.status_code == status.HTTP_200_OK
    assert "id" in response.json()


@pytest.mark.asyncio
async def test_read_graph(async_client):
    create_response = await async_client.post("/api/graph/", json=sample_graph)
    assert create_response.status_code == status.HTTP_200_OK
    graph_id = create_response.json()["id"]

    response = await async_client.get(f"/api/graph/{graph_id}")
    assert response.status_code == status.HTTP_200_OK
    assert "nodes" in response.json()


@pytest.mark.asyncio
async def test_get_adjacency_list(async_client):
    create_response = await async_client.post("/api/graph/", json=sample_graph)
    assert create_response.status_code == status.HTTP_200_OK
    graph_id = create_response.json()["id"]

    response = await async_client.get(f"/api/graph/{graph_id}/adjacency_list")
    assert response.status_code == status.HTTP_200_OK
    assert "adjacency_list" in response.json()


@pytest.mark.asyncio
async def test_get_reverse_adjacency_list(async_client):
    create_response = await async_client.post("/api/graph/", json=sample_graph)
    assert create_response.status_code == status.HTTP_200_OK
    graph_id = create_response.json()["id"]

    response = await async_client.get(f"/api/graph/{graph_id}/reverse_adjacency_list")
    assert response.status_code == status.HTTP_200_OK
    assert "adjacency_list" in response.json()


@pytest.mark.asyncio
async def test_delete_node(async_client):
    create_response = await async_client.post("/api/graph/", json=sample_graph)
    assert create_response.status_code == status.HTTP_200_OK
    graph_id = create_response.json()["id"]

    response = await async_client.delete(f"/api/graph/{graph_id}/node/B")
    assert response.status_code == status.HTTP_204_NO_CONTENT
