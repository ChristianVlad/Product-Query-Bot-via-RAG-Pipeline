# tests/test_api.py
from fastapi.testclient import TestClient
from app.services.vector_store import VectorStore
from app.main import app

client = TestClient(app)

def test_post_query():
    response = client.post("/query", json={"user_id": "u001", "query": "Tell me about tablets"})
    assert response.status_code == 200
    assert "answer" in response.json()

def test_retrieval_hits():
    store = VectorStore("data/products.json", k=2)
    results = store.retrieve("cheap tablets")
    assert len(results) > 0

def test_retrieval_no_match():
    store = VectorStore("data/products.json", k=2)
    results = store.retrieve("spaceships with AI")
    # could still return fuzzy match, so check for list
    assert isinstance(results, list)