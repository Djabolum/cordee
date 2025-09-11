import os
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel
from chromadb import PersistentClient

class ValexaEF:
    """Wrapper fastembed compatible Chroma
    - __call__(self, input: List[str]) -> List[List[float]]
    - Choisit un modèle supporté si FASTEMBED_MODEL n'est pas dispo localement.
    """
    def __init__(self, model: Optional[str] = None, cache_dir: Optional[str] = None):
        from fastembed import TextEmbedding
        want = (model or os.getenv("FASTEMBED_MODEL") or
                "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        try:
            lst = TextEmbedding.list_supported_models()
            supported = {getattr(m, "model", None) or m for m in lst}
        except Exception:
            supported = set()
        use = want if (not supported or want in supported) else (
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
            if "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2" in supported
            else next(iter(supported))
        )
        self.model = use
        self._fe = TextEmbedding(model_name=use, cache_dir=cache_dir)

    def __call__(self, input: List[str]) -> List[List[float]]:
        return [v for v in self._fe.embed(input)]

# ---- Init RAG ----
HF_CACHE = os.getenv("HF_HOME", "/opt/valexa/.cache/huggingface")
INDEX = os.getenv("RAG_INDEX_PATH", "/opt/valexa/index")
COL = os.getenv("RAG_COLLECTION", "valexa")

client = PersistentClient(path=INDEX)
ef = ValexaEF(cache_dir=HF_CACHE)

try:
    col = client.get_or_create_collection(name=COL, embedding_function=ef)
except TypeError:
    # Compatibility guard with older/newer Chroma signatures
    col = client.get_or_create_collection(name=COL, metadata=None, embedding_function=ef)

app = FastAPI(title="Cordée")

class UpsertPayload(BaseModel):
    ids: List[str]
    documents: List[str]
    metadatas: Optional[List[dict]] = None

class QueryPayload(BaseModel):
    query: str
    n_results: int = 5

@app.get("/health")
def health():
    return {"ok": True, "collection": COL, "model": getattr(ef, "model", None)}

@app.post("/upsert")
def upsert(p: UpsertPayload):
    if p.metadatas and len(p.metadatas) != len(p.ids):
        return {"ok": False, "error": "metadatas length must match ids length"}
    col.add(ids=p.ids, documents=p.documents, metadatas=p.metadatas)
    return {"ok": True, "count": len(p.ids)}

@app.post("/query")
def query(p: QueryPayload):
    res = col.query(query_texts=[p.query], n_results=p.n_results)
    return {"ok": True, "results": res}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("RAG_HOST","127.0.0.1"), port=int(os.getenv("RAG_PORT","8008")))
