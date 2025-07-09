# Product-Query Bot via RAG Pipeline

**Product-Query Bot** is a lightweight microservice that simulates a conversational assistant capable of answering user questions about products. It combines **Retrieval-Augmented Generation (RAG)** with a modular **multi-agent architecture** to deliver grounded and context-aware responses using **Large Language Models (LLMs)**.

---

## 📌 Overview

This project was developed as a technical assessment to demonstrate proficiency in:

- LLM-based agentic architectures
- Retrieval-Augmented Generation pipelines
- LangGraph and LangChain integration
- Prompt engineering and modular design
- Software engineering best practices (testing, Docker, clean code)

---

## ⚙️ Features

- FastAPI-based RESTful service
- Multi-agent orchestration using LangGraph
- Semantic search over embedded product corpus (FAISS)
- Dynamic prompt generation via OpenAI LLM
- Fully containerized (Docker)
- Configurable and testable architecture

---

## 🧱 Architecture

```plaintext
/product-query-bot/
├── app/
│ ├── main.py # FastAPI application
│ ├── agents/
│ │ ├── retriever.py # Retriever Agent (semantic retrieval)
│ │ └── responder.py # Responder Agent (LLM response generation)
│ ├── models/
│ │ └── schemas.py # Pydantic request models
│ ├── services/
│ │ ├── vector_store.py # FAISS vector indexing and retrieval
│ │ └── llm_service.py # LangChain + OpenAI integration
│ └── config.py # Environment and runtime configuration
├── tests/
│ ├── test_retrieval.py # Unit tests for vector store
│ ├── test_clasifier.py
│ └── test_api.py # API integration tests
├── data/ # Product documents (e.g., products.json)
├── Dockerfile # Docker image specification
├── docker-compose.yml # Optional container orchestration
├── requirements.txt # Python dependencies
├── .env.example # Environment variable template
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ChristianVlad/Product-Query-Bot-via-RAG-Pipeline.git
cd product-query-bot
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
cp .env.example .env
# Edit .env to include your OPENAI_API_KEY

### 5. Run the API
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. Example API Call
```bash
curl -X POST http://localhost:8000/query \
     -H "Content-Type: application/json" \
     -d '{"user_id": "abc123", "query": "What battery life does the smartwatch have?"}'
```

### 🐳 Docker Instructions
# Build the Docker Image
```bash
docker build -t product-query-bot .
```

## Run the Container
```bash
docker run -p 8000:8000 --env-file .env product-query-bot
```

### Test Suite
Run unit and integration tests using pytest:


### Core Components

| Component          | Description                                                                 |
| ------------------ | --------------------------------------------------------------------------- |
| `RetrieverAgent`   | Retrieves top-k relevant documents using semantic similarity (FAISS)        |
| `ResponderAgent`   | Constructs a prompt with retrieved context and generates a response via LLM |
| `LangGraph` Flow   | Manages multi-agent orchestration from retrieval to response                |
| `Vector Store`     | In-memory vector index built from product descriptions (JSON)               |
| `FastAPI` Endpoint | Accepts incoming JSON queries and triggers the pipeline                     |

### 📄 Environment Configuration
```env
OPENAI_API_KEY=your-api-key
TOP_K=3
```

### GET HTML Generate
```bash
pytest --html=report.html --self-contained-html
```

📬 Contact
For inquiries or collaboration:

Email: christian.valladaresp@gmail.com.com

GitHub: github.com/ChristianVlad

### TEST CASES

```bash
{
  "user_id": "user001",
  "answer": "The Zubale PowerBank 2 falls under the Accessories category and is priced at $49."
},
{
"user_id": "u001", 
"query": "What is the price of Zubale Mouse Inalámbrico?"
},
{
"user_id": "u002", 
"query": "What category does the Zubale Keyboard MX belong to?"
},
{"user_id": 
"u003", "query": "Tell me about the Backpack"
},
{
"user_id": 
"u004", "query": "What is the square root of 144?"
},
{
"user_id": 
"u005", "query": "What is the price of Samsung Galaxy S20?"
}
```bash
