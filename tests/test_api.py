# tests/test_retrieval.py
from app.services.vector_store import VectorStore
from fastapi.testclient import TestClient
from app.main import app

def test_retrieval():
    store = VectorStore("data/products.json", k=2)
    results = store.retrieve("cheap tablets")
    assert len(results) > 0

client = TestClient(app)

def test_post_query_valid():
    response = client.post("/query", json={"user_id": "u001", "query": "Tell me about tablets"})
    assert response.status_code == 200
    assert "answer" in response.json()

def test_post_query_general():
    response = client.post("/query", json={"user_id": "u002", "query": "What is 5 + 5?"})
    assert response.status_code == 200
    assert "answer" in response.json()
    assert "support team" in response.json()["answer"]

def test_post_query_invalid_schema():
    response = client.post("/query", json={"user": "bad_input"})
    assert response.status_code == 422


from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_known_product_query():
    response = client.post("/query", json={
        "user_id": "u100", 
        "query": "Tell me about the Zubale Tablet Go"
    })
    assert response.status_code == 200
    assert "answer" in response.json()
    assert "Tablet" in response.json()["answer"]

def test_fuzzy_product_query():
    response = client.post("/query", json={
        "user_id": "u101", 
        "query": "Price and category of PowerBank 20K?"
    })
    assert response.status_code == 200
    assert "Accessories" in response.json()["answer"] or "price" in response.json()["answer"].lower()

def test_general_query_fallback():
    response = client.post("/query", json={
        "user_id": "u102", 
        "query": "What's the square root of 144?"
    })
    assert response.status_code == 200
    assert "support team" in response.json()["answer"]

def test_missing_fields():
    response = client.post("/query", json={
        "user": "broken"
    })
    assert response.status_code == 422  # validation error

def test_empty_query():
    response = client.post("/query", json={
        "user_id": "u103", 
        "query": ""
    })
    assert response.status_code == 200
    assert "not sure" in response.json()["answer"].lower()


def test_exact_product_match():
    response = client.post("/query", json={"user_id": "u001", "query": "What is the price of Zubale Mouse Inalámbrico?"})
    assert response.status_code == 200
    assert "Inalámbrico" in response.json()["answer"]
    assert "$10" in response.json()["answer"]

def test_product_category_query():
    response = client.post("/query", json={"user_id": "u002", "query": "What category does the Zubale Keyboard MX belong to?"})
    assert response.status_code == 200
    assert "Periféricos" in response.json()["answer"]

def test_product_query_partial_name():
    response = client.post("/query", json={"user_id": "u003", "query": "Tell me about the Backpack"})
    assert response.status_code == 200
    assert "Mochila" in response.json()["answer"]

def test_non_product_math_question():
    response = client.post("/query", json={"user_id": "u004", "query": "What is the square root of 144?"})
    assert response.status_code == 200
    assert "support team" in response.json()["answer"].lower() or "ask the company" in response.json()["answer"].lower()

def test_product_not_found():
    response = client.post("/query", json={"user_id": "u005", "query": "What is the price of Samsung Galaxy S20?"})
    assert response.status_code == 200
    assert "not in our catalog" in response.json()["answer"].lower() or "support team" in response.json()["answer"].lower()

