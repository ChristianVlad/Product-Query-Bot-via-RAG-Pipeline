# app/agents/retriever.py
from typing import Dict
from app.services.vector_store import VectorStore
from app.utils.query_classifier import is_product_query

class RetrieverAgent:
    def __init__(self, vector_store: VectorStore):
        self.vs = vector_store

    def run(self, input: Dict) -> Dict:
        query = input["query"]
        docs = self.vs.retrieve(query)

        return {
            "user_id": input["user_id"],
            "query": query,
            "context": [doc.page_content for doc in docs]
        }
