from fastapi.testclient import TestClient
import importlib

def test_health():
    app = getattr(importlib.import_module("rag_http"), "app")
    with TestClient(app) as client:
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json().get("ok") is True
