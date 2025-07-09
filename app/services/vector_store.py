# app/services/vector_store.py
import json
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import Document
from app.models.product import Product

class VectorStore:
    def __init__(self, json_path: str, k: int = 3):
        self.k = k
        self.embeddings = OpenAIEmbeddings()
        self.store = self._load(json_path)

    def _load(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        validated = [Product(**item) for item in raw_data]
        docs = [
            Document(
                page_content=(
                    f"{p.name}. {p.description} "
                    f"Category: {p.category}. Price: {p.price}"
                ),
                metadata={"id": p.id}
            )
            for p in validated
        ]
        return FAISS.from_documents(docs, self.embeddings)

    def retrieve(self, query: str):
        return self.store.similarity_search(query, k=self.k)
