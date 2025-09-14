from fastapi.testclient import TestClient
import importlib
import os


def test_health():
    os.environ.setdefault("CORDEE_CI", "1")
    app = getattr(importlib.import_module("rag_http"), "app")
    with TestClient(app) as client:
        r = client.get("/health")
        assert r.status_code == 200
        body = r.json()
        assert body.get("ok") is True
        assert "collection" in body
        assert "model" in body


def test_query_offline():
    os.environ.setdefault("CORDEE_CI", "1")
    app = getattr(importlib.import_module("rag_http"), "app")
    with TestClient(app) as client:
        r = client.post("/query", json={"query": "hello", "n_results": 1})
        assert r.status_code == 200
        data = r.json()
        assert data.get("ok") is True
        assert "result" in data
        result = data["result"]
        assert "ids" in result and isinstance(result["ids"], list)
        assert "documents" in result and isinstance(result["documents"], list)
