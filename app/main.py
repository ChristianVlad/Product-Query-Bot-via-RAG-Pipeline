# app/main.py
from fastapi import FastAPI, HTTPException
from app.models.schemas import QueryRequest
from app.graph import build_graph

app = FastAPI(
    title="Product Query Bot via RAG",
    description="Microservice that answers product-related queries using LLMs and a RAG pipeline.",
    version="1.0.0"
)

graph = build_graph()

@app.get("/index")
def health_check():
    return {"status": "ok"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/query")
def query_handler(req: QueryRequest):
    try:
        result = graph.invoke({"user_id": req.user_id, "query": req.query})
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
