import pdfplumber
import io
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def extract_text_from_pdf_bytes(file_bytes: bytes) ->str:
    """Extraxt text from pdf bytes using pdfplumber"""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        pages = [p.extract_text() or "" for p in pdf.pages]
    return "\n".join(pages)

def chunk_text(text:str,chunk_size: int =1000,overlap: int = 200):
    """Split long text into overlapiong chunks """
    chunks = []
    start = 0
    L = len(text)
    while start < L:
        end = start + chunk_size
        chunks.append(text[start:end])
        start = max(end-overlap, end) 
    return chunks

def rank_chunk_by_query(chunks,query, top_k=5):
    """
    Simple TF_IDF + cosine similarity ranking of chunks to query.
    Return indices and stores
    """
    # vectorise chunk + query together

    vect = TfidfVectorizer().fit(chunks+[query])
    chunk_vecs = vect.transform(chunks)
    query_vec = vect.transform([query])
    sims = cosine_similarity(query_vec,chunk_vecs)[0]
    idxs = np.argsort(sims)[::-1][:top_k]
    return [(int(i),float(sims[i])) for i in idxs]