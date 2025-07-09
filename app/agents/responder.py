# app/agents/responder.py
from app.services.llm_service import call_llm

class ResponderAgent:
    def run(self, input: dict) -> dict:
        context = "\n".join(input["context"])
        context_type = input.get("context_type", "product")

        if context_type == "general":
            return {
                "user_id": input["user_id"],
                "answer": (
                    "This question doesn't seem related to our product catalog. "
                    "Let me check with our support team for you."
                )
            }

        prompt = (
            "You are a helpful assistant. Answer the following customer question "
            "using only the context provided below. "
            "If the answer cannot be found, respond with: "
            "\"I'm not sure, let me ask the company for clarification.\"\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {input['query']}"
        )

        answer = call_llm(prompt)
        return {
            "user_id": input["user_id"],
            "answer": answer
        }
