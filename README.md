# Product-Query RAG Service

A retrieval-augmented question-answering service for product catalogs, built around a two-agent architecture (retrieval and response generation) rather than a single monolithic LLM call. Designed to demonstrate how a RAG pipeline should be *structured* for production — not just wired together — including evaluation, containerization, and a graceful-degradation path when retrieval finds nothing relevant.

---

## Why two agents instead of one prompt?

Most RAG demos collapse retrieval and generation into a single function call. That works for a demo; it breaks down when you need to:

- Swap the retrieval strategy (similarity search → hybrid search → re-ranking) without touching generation logic
- Unit-test retrieval quality independently from response quality
- Add a moderation/guardrail step between "what we found" and "what we say"

This project splits the pipeline into a **Retriever Agent** and a **Responder Agent**, orchestrated through LangGraph. Each agent has a single responsibility and can be evaluated, replaced, or scaled independently.

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   FastAPI   │────▶│ Retriever Agent │────▶│  Responder Agent │
│   /query    │     │  (FAISS semantic │     │  (LLM + context  │
│   endpoint  │     │   search, top-k) │     │   construction)  │
└─────────────┘     └──────────────────┘     └──────────────────┘
                              │                         │
                              ▼                         ▼
                     ┌─────────────────┐      ┌──────────────────┐
                     │ Vector Store    │      │   OpenAI API     │
                     │ (product corpus)│      │  (response gen)  │
                     └─────────────────┘      └──────────────────┘
```

LangGraph manages the flow between agents, including the out-of-scope case: when a query has no relevant match in the product corpus (e.g. *"What is the square root of 144?"*), the graph routes to a fallback response instead of forcing the LLM to hallucinate a product answer.

---

## What this demonstrates

| Concern | How it's handled here |
|---|---|
| **Grounding** | Responses are constructed only from retrieved context — the Responder Agent never answers from parametric knowledge alone |
| **Separation of concerns** | Retrieval and generation are independently testable units, not one prompt |
| **Out-of-scope handling** | Queries unrelated to the product corpus are detected and routed to a fallback, not silently hallucinated |
| **Observability path** | Test suite includes retrieval-quality tests (`test_retrieval.py`) separate from end-to-end API tests (`test_api.py`) |
| **Containerized & config-driven** | Runtime behavior (top-k, model choice) is environment-driven, not hardcoded |

---

## Architecture

```
app/
├── main.py                 # FastAPI application entrypoint
├── agents/
│   ├── retriever.py        # Retriever Agent — semantic search over product corpus
│   └── responder.py        # Responder Agent — grounded LLM response generation
├── models/
│   └── schemas.py          # Pydantic request/response contracts
├── services/
│   ├── vector_store.py     # FAISS indexing and retrieval
│   └── llm_service.py      # LangChain + OpenAI integration
└── config.py                # Environment and runtime configuration

tests/
├── test_retrieval.py        # Retrieval-quality unit tests
├── test_classifier.py       # Query classification tests
└── test_api.py               # End-to-end API integration tests
```

---

## Running it locally

```bash
git clone https://github.com/ChristianVlad/Product-Query-Bot-via-RAG-Pipeline.git
cd Product-Query-Bot-via-RAG-Pipeline

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # add your OPENAI_API_KEY
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Or with Docker:

```bash
docker build -t product-query-bot .
docker run -p 8000:8000 --env-file .env product-query-bot
```

### Example request

```bash
curl -X POST http://localhost:8000/query \
     -H "Content-Type: application/json" \
     -d '{"user_id": "abc123", "query": "What battery life does the smartwatch have?"}'
```

### Running tests

```bash
pytest --html=report.html --self-contained-html
```

---

## Design decisions & trade-offs

- **FAISS in-memory rather than a managed vector DB.** Right call for a bounded product catalog where the index rebuilds in seconds; the retrieval layer (`vector_store.py`) is abstracted so swapping in Pinecone/Weaviate for a larger corpus is a config change, not a rewrite.
- **LangGraph over a plain LangChain chain.** A linear chain can't express the "no relevant match → fallback" branch cleanly. The graph makes the control flow explicit and testable as its own unit.
- **Pydantic schemas at the API boundary.** Keeps the contract between FastAPI and the agent layer strict, so changes to the LLM prompt or retrieval logic don't silently break the API shape.

## What I'd add for a production version

- Re-ranking step after initial FAISS retrieval (cross-encoder) to improve precision on ambiguous queries
- Structured logging of retrieval scores per query, to catch silent retrieval-quality degradation
- A persistent vector store + incremental indexing, instead of rebuilding the index on startup

---

## Stack

`FastAPI` · `LangGraph` · `LangChain` · `FAISS` · `OpenAI API` · `Pydantic` · `Docker` · `pytest`

---

## Contact

Christian Peña — [LinkedIn](https://www.linkedin.com/in/christian-vp/) · [christian.valldaresp@gmail.com](mailto:christian.valldaresp@gmail.com)
