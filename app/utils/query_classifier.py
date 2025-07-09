from typing import Literal
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import Document
from app.config import settings
import json
import os

PRODUCT_TOPICS = [
    "tablet", "smartphone", "mouse", "accessories", "devices", "tech", "product", "electronics",
    "battery", "price", "specs", "screen", "charger", "Bluetooth", "wireless", "usb"
]

embedding_model = OpenAIEmbeddings()

def is_product_query(query: str, threshold: float = 0.7) -> bool:
    """
    Returns True if the query appears product-related.
    Uses simple semantic similarity against keywords.
    """
    query_embedding = embedding_model.embed_query(query)

    # Construct minimal synthetic doc set
    documents = [Document(page_content=kw) for kw in PRODUCT_TOPICS]
    temp_store = FAISS.from_documents(documents, embedding_model)
    results = temp_store.similarity_search_with_score(query, k=1)

    if results and results[0][1] >= threshold:
        return True
    return False