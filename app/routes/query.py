from fastapi import APIRouter
from app.models import QueryRequest
from app.db import documents_col
from app.utils import rank_chunk_by_query
import os
import requests
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER")
GROQ_KEY = os.getenv("GROQ_KEY")

router = APIRouter(prefix="/qa",tags=["qa"])

def call_groq(prompt: str):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300,
        "temperature": 0.2
    }

    r = requests.post(url, json=payload, headers=headers, timeout=30)
    print("DEBUG:", r.text)   # debug
    r.raise_for_status()
    j = r.json()

    # return the LLM's reply
    return j["choices"][0]["message"]["content"]



@router.post("/query")
def query(req: QueryRequest):
    # fetch all documents (in a real app filter by doc id or user)
    docs = list(documents_col.find({}, {"title":1, "chunks":1}))
    # flatten chunks with reference to doc/title
    all_chunks = []
    meta = []
    for d in docs:
        title = d.get("title", "untitled")
        for i, ch in enumerate(d.get("chunks", [])):
            all_chunks.append(ch)
            meta.append({"doc_id": d["_id"], "title": title, "chunk_index": i})

    if not all_chunks:
        return {"answer": "No documents uploaded yet."}

    # rank chunks
    ranked = rank_chunk_by_query(all_chunks, req.question, top_k=req.top_k)
    # build context string from top chunks
    top_texts = []
    for idx, score in ranked:
        top_texts.append(f"--- chunk (score={score:.3f}) ---\n{all_chunks[idx]}")

    context = "\n\n".join(top_texts)
    prompt = f"Use the following context to answer the question. Be concise.\n\nContext:\n{context}\n\nQuestion: {req.question}\nAnswer:"

    # call LLM provider depending on environment
    answer = call_groq(prompt)

    return {"answer": answer, "sources": [meta[int(i)] for i,_ in ranked]}