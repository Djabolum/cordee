import os
from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chromadb import PersistentClient
try:
    from chromadb import EphemeralClient
except Exception:
    EphemeralClient = None

# Determine if we are in CI/offline mode
CI_MODE = os.getenv("CORDEE_CI") == "1"

# Environment variables and defaults
CHROMA_PATH = os.getenv("CHROMA_PATH", "/opt/cordee/index")
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "cordee")
MODEL_NAME = os.getenv("FASTEMBED_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

app = FastAPI()

# Lazy-initialized singletons
_client = None
_collection = None
_embedder = None

def get_client():
    global _client
    if _client is None:
        if CI_MODE and EphemeralClient is not None:
            # Use an in-memory Chroma client in CI to avoid persistence and disk IO
            _client = EphemeralClient()
        else:
            _client = PersistentClient(path=CHROMA_PATH)
    return _client

def get_collection():
    global _collection
    if _collection is None:
        client = get_client()
        # Create or get the collection without specifying embedding function here
        _collection = client.get_or_create_collection(name=CHROMA_COLLECTION)
    return _collection

class DummyEmbedder:
    """A minimal embedder that returns deterministic vectors for tests."""
    def __call__(self, input):
        if isinstance(input, str):
            input = [input]
        return [[0.0] * 8 for _ in input]  # 8-dim zero vectors

def get_embedder():
    global _embedder
    if _embedder is None:
        if CI_MODE:
            # Use dummy embedder in CI to avoid downloading real model
            _embedder = DummyEmbedder()
        else:
            from fastembed import TextEmbedding
            _embedder = TextEmbedding(model_name=MODEL_NAME)
    return _embedder

# Pydantic models for request bodies
class UpsertPayload(BaseModel):
    ids: List[str]
    documents: List[str]
    metadatas: List[Dict] | None = None

class QueryPayload(BaseModel):
    query: str
    n_results: int = 5

@app.get("/health")
def health():
    """Health endpoint with minimal side effects."""
    return {"ok": True, "collection": CHROMA_COLLECTION, "model": MODEL_NAME}

@app.post("/upsert")
def upsert(payload: UpsertPayload):
    # Validate lengths
    if payload.metadatas is not None and len(payload.metadatas) != len(payload.ids):
        raise HTTPException(status_code=400, detail="metadatas length must match ids length")
    # Lazy init embedder and collection
    embedder = get_embedder()
    collection = get_collection()
    embeddings = embedder(payload.documents)
    # Add to collection
    collection.add(ids=payload.ids, documents=payload.documents, metadatas=payload.metadatas, embeddings=embeddings)
    return {"ok": True, "n": len(payload.ids)}

@app.post("/query")
def query(payload: QueryPayload):
    embedder = get_embedder()
    collection = get_collection()
    embeddings = embedder([payload.query])
    result = collection.query(query_embeddings=embeddings, n_results=payload.n_results)
    return {"ok": True, "result": result}
