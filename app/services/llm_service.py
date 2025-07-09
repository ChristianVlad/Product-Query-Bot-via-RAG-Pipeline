# app/services/llm_service.py
from langchain_community.chat_models import ChatOpenAI
from app.config import settings

def call_llm(prompt: str) -> str:
    llm = ChatOpenAI(
        model_name=settings.LLM_MODEL,
        temperature=0,
        openai_api_key=settings.OPENAI_API_KEY
    )
    return llm.predict(prompt)
