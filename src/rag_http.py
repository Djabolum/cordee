import os
from typing import List, Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

try:
    from chromadb import PersistentClient, EphemeralClient
except Exception:  # pragma: no cover - defensive import
    from chromadb import PersistentClient

    EphemeralClient = None  # type: ignore


# ---- Environment ----
def _truthy(val: Optional[str]) -> bool:
    if val is None:
        return False
    return str(val).strip().lower() not in ("", "0", "false", "no", "off")


CI_MODE = _truthy(os.getenv("CORDEE_CI"))
# Silence Chroma telemetry in dev/CI unless explicitly enabled
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")
# Support legacy env names from earlier docs/systemd
CHROMA_PATH = os.getenv("CHROMA_PATH", os.getenv("RAG_INDEX_PATH", "/opt/cordee/index"))
CHROMA_COLLECTION = os.getenv(
    "CHROMA_COLLECTION", os.getenv("RAG_COLLECTION", "cordee")
)
MODEL_NAME = os.getenv(
    "FASTEMBED_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
HF_CACHE = os.getenv("HF_HOME") or os.getenv("HUGGINGFACE_HUB_CACHE")

app = FastAPI()

# ---- Lazy singletons ----
_client = None
_collection = None
_embedder = None


def ci_mode() -> bool:
    """Read CI mode dynamically from env for robustness."""
    return _truthy(os.getenv("CORDEE_CI"))


def get_client():
    global _client
    if _client is None:
        if ci_mode() and EphemeralClient is not None:
            _client = EphemeralClient()
        else:
            _client = PersistentClient(path=CHROMA_PATH)
    return _client


def get_collection():
    global _collection
    if _collection is None:
        client = get_client()
        _collection = client.get_or_create_collection(name=CHROMA_COLLECTION)
    return _collection


class DummyEmbedder:
    """Deterministic tiny embedder for offline/CI mode."""

    def __init__(self, dim: int = 8):
        self.dim = dim
        self.model = f"dummy-{dim}"

    def __call__(self, input: List[str]) -> List[List[float]]:
        if isinstance(input, str):
            input = [input]
        return [[0.0] * self.dim for _ in input]


def get_embedder():
    global _embedder
    if _embedder is None:
        if ci_mode() or _truthy(os.getenv("FORCE_DUMMY_EMBED")):
            _embedder = DummyEmbedder()
        else:
            from fastembed import TextEmbedding

            _embedder = TextEmbedding(model_name=MODEL_NAME, cache_dir=HF_CACHE)
            # Expose model name if available for /health
            try:
                _embedder.model = MODEL_NAME  # type: ignore[attr-defined]
            except Exception:
                pass
    return _embedder


# ---- Schemas ----
class UpsertPayload(BaseModel):
    ids: List[str]
    documents: List[str]
    metadatas: List[Dict] | None = None


class QueryPayload(BaseModel):
    query: str
    n_results: int = 5


# ---- Routes ----
@app.get("/health")
def health():
    emb = get_embedder()
    model = getattr(emb, "model", MODEL_NAME)
    return {"ok": True, "collection": CHROMA_COLLECTION, "model": str(model)}


@app.post("/upsert")
def upsert(payload: UpsertPayload):
    if payload.metadatas is not None and len(payload.metadatas) != len(payload.ids):
        raise HTTPException(
            status_code=400, detail="metadatas length must match ids length"
        )
    embedder = get_embedder()
    collection = get_collection()
    embeddings = embedder(payload.documents)
    collection.add(
        ids=payload.ids,
        documents=payload.documents,
        metadatas=payload.metadatas,
        embeddings=embeddings,
    )
    return {"ok": True, "n": len(payload.ids)}


@app.post("/query")
def query(payload: QueryPayload):
    embedder = get_embedder()
    collection = get_collection()
    qemb = embedder([payload.query])
    result = collection.query(query_embeddings=qemb, n_results=payload.n_results)
    return {"ok": True, "result": result}


if __name__ == "__main__":  # pragma: no cover - manual run helper
    import uvicorn

    host = os.getenv("RAG_HOST", "127.0.0.1")
    try:
        port = int(os.getenv("RAG_PORT", "8008"))
    except ValueError:
        port = 8008
    uvicorn.run(app, host=host, port=port)
