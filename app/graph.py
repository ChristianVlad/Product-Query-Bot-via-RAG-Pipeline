# app/graph.py
from langgraph.graph import StateGraph
from app.agents.retriever import RetrieverAgent
from app.agents.responder import ResponderAgent
from app.services.vector_store import VectorStore
from app.config import settings

vector_store = VectorStore("data/products.json", k=settings.TOP_K)
retriever = RetrieverAgent(vector_store)
responder = ResponderAgent()

def build_graph():
    workflow = StateGraph(dict)
    workflow.add_node("retrieve", retriever.run)
    workflow.add_node("respond", responder.run)
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "respond")
    workflow.set_finish_point("respond")
    return workflow.compile()