import ollama
from config.settings import LLM_MODEL

def generate_answer(context: str, question: str):
    prompt = f"""
Based on the context below, answer the question.

Context:
{context}

Question:
{question}

Answer:
"""

    response = ollama.generate(
        model=LLM_MODEL,
        prompt=prompt
    )

    return response["response"]
