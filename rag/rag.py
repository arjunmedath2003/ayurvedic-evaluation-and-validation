from vector_store import VectorStore
from evidence import format_evidence
from llm_ollama import generate_answer
import numpy as np

SYSTEM_PROMPT = """
You are an expert in Ayurvedic pharmacology and systems biology.

Rules:
- Use ONLY the evidence provided.
- Do NOT add external knowledge.
- If information is missing, say "Not found in the data".
- Cite evidence as [E1], [E2], etc.
"""

store = VectorStore("ayurveda.index", "chunks.json")

def answer_question(query: str, query_embedding: np.ndarray, k=20):
    retrieved_chunks = store.search(query_embedding, k=k)
    evidence = format_evidence(retrieved_chunks)

    prompt = f"""
        {SYSTEM_PROMPT}

        Evidence:
        {evidence}

        Question:
        {query}
    """
    return generate_answer(prompt)
    # return evidence