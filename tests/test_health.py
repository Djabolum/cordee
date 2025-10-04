from fastapi.testclient import TestClient
import importlib
import os


def _load_app(tmp_path):
    # Ensure CI mode and a writable CHROMA_PATH for tests
    os.environ.setdefault("CORDEE_CI", "1")
    os.environ.setdefault("CHROMA_PATH", str(tmp_path / "index"))
    mod = importlib.import_module("rag_http")
    # Reload to pick up env if module was already imported
    mod = importlib.reload(mod)
    return getattr(mod, "app")


def test_health(tmp_path):
    app = _load_app(tmp_path)
    with TestClient(app) as client:
        r = client.get("/health")
        assert r.status_code == 200
        body = r.json()
        assert body.get("ok") is True
        assert "collection" in body
        assert "model" in body


def test_query_offline(tmp_path):
    app = _load_app(tmp_path)
    with TestClient(app) as client:
        r = client.post("/query", json={"query": "hello", "n_results": 1})
        assert r.status_code == 200
        data = r.json()
        assert data.get("ok") is True
        assert "result" in data
        result = data["result"]
        assert "ids" in result and isinstance(result["ids"], list)
        assert "documents" in result and isinstance(result["documents"], list)
